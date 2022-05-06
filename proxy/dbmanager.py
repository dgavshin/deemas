from os import getenv
from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from utils import log

engine = create_engine(getenv("SQLALCHEMY_DATABASE_URI", "sqlite:///proxy.db"))
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

from entities import *
from dto import BooleanOperator as ProxyBooleanOperator
from dto import ActionType as ProxyActionType
from dto import RuleProtocol as ProxyProtocol
from dto import Service, ScriptRule, ConditionRule


def map_script_rule(script_rule: ScriptRuleEntity) -> Optional[ScriptRule]:
    try:
        log.debug("Script rule mapping: " + script_rule.name)
        return ScriptRule(order=script_rule.order,
                          boolean_operator=ProxyBooleanOperator[script_rule.boolean_operator.name],
                          script=script_rule.script,
                          name=script_rule.name,
                          action_type=ProxyActionType[script_rule.action_type.name],
                          protocol=ProxyProtocol[script_rule.protocol.value])
    except Exception as e:
        log.error(f"Не удалось инициализировать script правило {script_rule.name}: " + str(e))


def map_condition_rule(condition_rule: ConditionRuleEntity) -> Optional[ConditionRule]:
    try:
        log.debug("Condition rule mapping: %s %s %s in %s"
                  % (condition_rule.match_type, condition_rule.match_relationship, condition_rule.match_condition,
                     condition_rule.match_side))
        return ConditionRule(order=condition_rule.order,
                             match_side=condition_rule.match_side,
                             match_condition=condition_rule.match_condition,
                             match_type=condition_rule.match_type,
                             match_relationship=condition_rule.match_relationship,
                             boolean_operator=ProxyBooleanOperator[condition_rule.boolean_operator.name],
                             action_type=ProxyActionType[condition_rule.action_type.name],
                             protocol=ProxyProtocol[condition_rule.protocol.value])
    except Exception as e:
        log.error("Не удалось инициализировать condition правило: " + str(e))


def map_service(service: ServiceEntity) -> Service:
    log.debug("Service mapping: %s" % service.name)
    mapped_condition_rules = [map_condition_rule(rule) for rule in service.condition_rules if rule.enabled]
    mapped_script_rules = [map_script_rule(rule) for rule in service.script_rules if rule.enabled]
    return Service(name=service.name, condition_rules=mapped_condition_rules, script_rules=mapped_script_rules,
                   rule_operator=ProxyBooleanOperator[service.rule_operator.name])


def get_service(name: str) -> Service:
    return map_service(session
                       .query(ServiceEntity)
                       .filter(ServiceEntity.name == name)
                       .one_or_none())
