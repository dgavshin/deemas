import enum
import importlib.util
import os
import tempfile
import typing
from dataclasses import dataclass, field
from inspect import signature
from pathlib import Path
from types import ModuleType, FunctionType

from mitmproxy.http import HTTPFlow
from mitmproxy.tcp import TCPFlow

from conditions import protocol_conditions, ConditionOption
from utils import log


class BooleanOperator(enum.Enum):
    AND = ("AND", lambda left, right: left and right)
    OR = ("OR", lambda left, right: left or right)

    def operator(self, left, right):
        return self.value[1](left, right)


class RuleProtocol(enum.Enum):
    TCP = TCPFlow
    HTTP = HTTPFlow

    def __init__(self, flow_type):
        self.flow_type = flow_type

    def name(self):
        return self._name_


class ActionType(enum.Enum):
    ENCRYPT = "encrypt"
    DECRYPT = "decrypt"


class RuleType(enum.Enum):
    SCRIPT = "script"
    CONDITION = "condition"


@dataclass
class Rule:
    order: int
    action_type: ActionType
    boolean_operator: BooleanOperator

    def check(self, flow) -> bool:
        pass


@dataclass
class ScriptRule(Rule):
    name: str
    script: str
    protocol: RuleProtocol
    module: ModuleType = field(init=False)

    def __post_init__(self):
        self.module = self.create_module()

    def check(self, flow) -> bool:
        return self.module.check(flow)

    def create_module(self):
        if not isinstance(self.script, Path):
            temp_path = Path(tempfile.gettempdir(), self.name + ".py")
            with open(temp_path, "w") as f:
                f.write(self.script)
        else:
            temp_path = self.script

        spec = importlib.util.spec_from_file_location(self.name, temp_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.validate_module(module)
        os.remove(temp_path)
        return module

    def validate_module(self, module: ModuleType):
        """
        Валидирует правила по следующим критериям:
            1. у правила (модуля) есть метод check
            2. метод check имеет только 1 параметр
            3. тип этого параметра должен быть наследником класса proxy.flow.Flow
            4. тип возвращаемого значения - bool
        """
        if not hasattr(module, "check") or not isinstance(module.check, FunctionType):
            raise ValueError(f"У правила {self.name} нет метода check(flow: HTTPFlow)")
        s = signature(module.check)
        if len(s.parameters) != 1:
            raise ValueError(f"У правила {self.name} не 1 параметр")
        parameter_name = list(s.parameters.keys())[0]
        if s.parameters.get(parameter_name).annotation != self.protocol.flow_type:
            raise ValueError(f"У правила {self.name} тип параметра не {self.protocol.flow_type}")
        if s.return_annotation != bool:
            raise ValueError(f"У правила {self.name} тип возвращаемого значения не bool")


@dataclass
class ConditionRule(Rule):
    supplier: typing.Callable = field(init=False)
    matcher: typing.Callable = field(init=False)

    protocol: RuleProtocol
    match_type: str
    match_relationship: str
    match_condition: str
    match_side: str

    def __post_init__(self):
        log.debug(f"[{self.match_type}] Condition rule post init")
        option: ConditionOption = protocol_conditions.get(self.protocol.name())[self.match_type]
        self.supplier = option.supplier
        self.matcher = option.matcher

    def check(self, flow) -> bool:
        log.info(f"[{self.protocol}] {self.match_type} {self.match_relationship} {self.match_condition}"
                 f" in {self.match_side}")
        result = self.matcher(self.supplier, self.match_condition, self.match_relationship,
                              flow=flow, match_side=self.match_side)
        return result


@dataclass
class Service:
    name: str
    condition_rules: list[ConditionRule]
    script_rules: list[ScriptRule]
    rule_operator: BooleanOperator

    def fill_rules(self, incoming_rules, rule_type: RuleType):
        for rule in filter(lambda x: x is not None, incoming_rules):
            if getattr(rule, "action_type") and isinstance(rule.action_type, ActionType):
                getattr(self, f"{rule.action_type.value}_{rule_type.value}_rules").append(rule)

    def __post_init__(self):
        self.condition_rules.sort(key=lambda c: c.order)
        self.validate_conditions_order()

        self.encrypt_condition_rules = []
        self.decrypt_condition_rules = []
        self.encrypt_script_rules = []
        self.decrypt_script_rules = []

        self.fill_rules(self.condition_rules, RuleType.CONDITION)
        self.fill_rules(self.script_rules, RuleType.SCRIPT)

    @staticmethod
    def process_rules(rules: list[Rule], flow) -> bool:
        if not rules:
            return True
        result = rules[0].check(flow)
        for rule in rules[1:]:
            result = rule.boolean_operator.operator(result, rule.check(flow))
        return result

    def decrypt_decision(self, flow):
        return self.rule_operator.operator(
            Service.process_rules(self.decrypt_condition_rules, flow),
            Service.process_rules(self.decrypt_script_rules, flow))

    def encrypt_decision(self, flow):
        return self.rule_operator.operator(
            Service.process_rules(self.encrypt_condition_rules, flow),
            Service.process_rules(self.encrypt_script_rules, flow))

    def validate_conditions_order(self):
        idx = 0
        for condition in self.condition_rules:
            if condition.order != idx:
                raise ValueError("Неверный порядок условий для правила:"
                                 f"условие \"{condition.match_type}\" должно быть с индексом {idx}")
            idx += 1
