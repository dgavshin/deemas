import re
from os.path import splitext
from typing import Callable, Iterable
from urllib.parse import urlparse, unquote

MATCHES = "Matches"
DOES_NOT_MATCH = "Does not match"

CONTAINS = "contains"
DOES_NOT_CONTAIN = "Does not contain"

default_match_relationship = (MATCHES, DOES_NOT_MATCH)
contain_match_relationships = (CONTAINS, DOES_NOT_CONTAIN)

URL = "URL"
BODY = "Body"
QUERY_PARAMS = "Query params"
PROTOCOL = "Protocol"
IP_ADDRESS = "IP address"
ANY_HEADER = "Any header"
PARAM_NAME = "Param name"
HOSTNAME = "Hostname"
PARAM_VALUE = "Param value"
LISTEN_PORT = "Listen port"
HTTP_METHOD = "HTTP method"
COOKIE_NAME = "Cookie name"
COOKIE_VALUE = "Cookie value"
FILE_EXTENSION = "File extension"

REQUEST_SIDE = "request"
RESPONSE_SIDE = "response"
default_match_sides = (REQUEST_SIDE, RESPONSE_SIDE)

CLIENT_CONNECTION = {"client_conn"}
SERVER_CONNECTION = {"server_conn"}
connection_sides = (CLIENT_CONNECTION, SERVER_CONNECTION)


def regex_matcher(supplier, match_condition, match_relationship, **kwargs):
    from utils import log

    value = str(supplier(**kwargs))
    log.debug(f"supplier result: {value if len(value) < 40 else str(value[:40] + '...')}")
    has_match = re.search(match_condition, value) is not None

    log.debug(f"{has_match=}")
    decision = has_match == (match_relationship is MATCHES)
    log.debug(f"{decision=}")
    return decision


def contain_matcher(supplier, match_condition, match_relationship, **kwargs):
    has_parameter = any(re.search(match_condition, value) for value in supplier(**kwargs))
    return has_parameter == (match_relationship is CONTAINS)


class ConditionOption:

    def __init__(self,
                 supplier: Callable,
                 matcher: Callable = regex_matcher,
                 match_relationships: Iterable = default_match_relationship,
                 match_sides: Iterable = default_match_sides
                 ):
        self.supplier = supplier
        self.matcher = matcher
        self.match_relationships = match_relationships
        self.match_sides = match_sides

    def serialize(self, match_type):
        return {"match_type": match_type, "match_sides": self.match_sides,
                "match_relationships": self.match_relationships}


http_conditions = {
    HOSTNAME: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).host),
    HTTP_METHOD: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).method,
                                 match_sides=(REQUEST_SIDE,)),
    URL: ConditionOption(supplier=lambda flow, match_side: unquote(getattr(flow, match_side).url),
                         match_sides=(REQUEST_SIDE,)),
    FILE_EXTENSION: ConditionOption(
        supplier=lambda flow, match_side: splitext(urlparse(getattr(flow, match_side).url).path)[1],
        match_sides=(REQUEST_SIDE,)),
    BODY: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).content.decode(encoding="UTF-8")),
    LISTEN_PORT: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).port),

    COOKIE_NAME: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).cookies.keys(),
                                 matcher=contain_matcher,
                                 match_relationships=contain_match_relationships),
    COOKIE_VALUE: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).cookies.values(),
                                  matcher=contain_matcher,
                                  match_relationships=contain_match_relationships),
    ANY_HEADER: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).headers.keys(),
                                matcher=contain_matcher,
                                match_relationships=contain_match_relationships),
    PARAM_NAME: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).json().keys(),
                                matcher=contain_matcher,
                                match_relationships=contain_match_relationships,
                                match_sides=(REQUEST_SIDE,)),
    PARAM_VALUE: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).json().values(),
                                 matcher=contain_matcher,
                                 match_relationships=contain_match_relationships,
                                 match_sides=(REQUEST_SIDE,)),

}

tcp_conditions = {
    HOSTNAME: ConditionOption(supplier=lambda flow, match_side: getattr(flow, match_side).peername[0],
                              match_sides=connection_sides),
    LISTEN_PORT: ConditionOption(supplier=lambda flow, match_side: str(getattr(flow, match_side).peername[1]),
                                 match_sides=connection_sides),
    BODY: ConditionOption(
        supplier=lambda flow, match_side:
        flow.messages[-1].content.decode(encoding="UTF-8")
        if (flow.messages[-1].from_client and match_side is REQUEST_SIDE) or (
                not flow.messages[-1].from_client and match_side is RESPONSE_SIDE)
        else None
    )
}

protocol_conditions = {"TCP": tcp_conditions, "HTTP": http_conditions, "tcp": tcp_conditions, "http": http_conditions}
