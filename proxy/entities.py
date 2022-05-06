from enum import Enum
from typing import List

from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import relationship

from dbmanager import Base


class Protocol(str, Enum):
    TCP = "TCP"
    HTTP = "HTTP"


class ActionType(str, Enum):
    ENCRYPT = "ENCRYPT"
    DECRYPT = "DECRYPT"


class BooleanOperator(str, Enum):
    AND = "AND"
    OR = "OR"


class ServiceEntity(Base):
    __tablename__ = "services"

    name: str = Column(String, primary_key=True)
    lang: str = Column(String, nullable=False)
    rule_operator: BooleanOperator = Column(SQLEnum(BooleanOperator), default=BooleanOperator.OR)
    condition_rules: List["ConditionRuleEntity"] = relationship("ConditionRuleEntity", back_populates="service")
    script_rules: List["ScriptRuleEntity"] = relationship("ScriptRuleEntity", back_populates="service")


class ConditionRuleEntity(Base):
    __tablename__ = "condition_rules"

    id: int = Column(Integer, primary_key=True)
    service_name = Column(String, ForeignKey('services.name'))
    service: ServiceEntity = relationship("ServiceEntity", back_populates="condition_rules")

    order = Column(Integer)
    protocol: Protocol = Column(SQLEnum(Protocol), nullable=False)
    enabled = Column(Boolean, default=False)
    boolean_operator: BooleanOperator = Column(SQLEnum(BooleanOperator), nullable=True)
    match_type = Column(String, nullable=False)
    match_relationship = Column(String, nullable=False)
    match_condition = Column(String, nullable=False)
    match_side = Column(String, nullable=False)
    action_type: ActionType = Column(SQLEnum(ActionType), nullable=False)


class ScriptRuleEntity(Base):
    __tablename__ = "script_rules"

    name: str = Column(String, primary_key=True)
    protocol: Protocol = Column(SQLEnum(Protocol), nullable=False)
    service_name: str = Column(String, ForeignKey('services.name'))
    service: ServiceEntity = relationship("ServiceEntity", back_populates="script_rules")
    action_type: ActionType = Column(SQLEnum(ActionType), nullable=False)
    enabled = Column(Boolean, default=False)

    order: int = Column(Integer)
    script: str = Column(String, nullable=False)
    boolean_operator: BooleanOperator = Column(SQLEnum(BooleanOperator), nullable=True)
