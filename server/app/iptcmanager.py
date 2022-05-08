import iptc

from server.app import app
from server.app.models import Service

chain = iptc.Chain(iptc.Table(iptc.Table.NAT), "PREROUTING")


def is_redirect_enabled(service: Service) -> bool:
    try:
        return create_redirect_rule(service) in chain.rules
    except Exception as e:
        raise ValueError(f"Не удалось проверить, включено ли правило для сервиса {service.name}: " + str(e))


def insert_redirect_rule(service: Service) -> None:
    try:
        if is_redirect_enabled(service):
            raise ValueError("Redirect правило уже включено")
        chain.insert_rule(create_redirect_rule(service))
    except Exception as e:
        raise ValueError(f"Не удалось добавить правило для сервиса {service.name}: " + str(e))


def delete_redirect_rule(service: Service) -> None:
    try:
        if not is_redirect_enabled(service):
            raise ValueError(f"Для сервиса {service.name} нет redirect правила")
        chain.delete_rule(create_redirect_rule(service))
    except Exception as e:
        raise ValueError(f"Не удалось удалить правило для сервиса {service.name}: " + str(e))


def create_redirect_rule(service: Service) -> iptc.Rule:
    rule = iptc.Rule()
    rule.protocol = 'tcp'
    rule.in_interface = app.config["INTERFACE"]
    rule.dport = str(service.proxy_port)
    rule.target = iptc.Target(rule, 'REDIRECT')
    rule.target.to_ports = str(service.port)
    return rule
