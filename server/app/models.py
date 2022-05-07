from enum import Enum
from typing import List

from sqlalchemy.sql import exists
from werkzeug.exceptions import NotFound

from server.app import db


class Protocol(str, Enum):
    TCP = "TCP"
    HTTP = "HTTP"


class ActionType(str, Enum):
    ENCRYPT = "ENCRYPT"
    DECRYPT = "DECRYPT"


class BooleanOperator(str, Enum):
    AND = "AND"
    OR = "OR"


class Service(db.Model):
    __tablename__ = "services"

    name = db.Column(db.String, primary_key=True)
    lang = db.Column(db.String, nullable=False)
    port = db.Column(db.Integer, unique=True, nullable=False)
    proxy_port = db.Column(db.Integer, nullable=False)
    proxy_host = db.Column(db.String, nullable=False)
    proxy_enabled = db.Column(db.Boolean, default=False)
    protocol: Protocol = db.Column(db.Enum(Protocol), nullable=False)
    rule_operator: BooleanOperator = db.Column(db.Enum(BooleanOperator), default=BooleanOperator.OR)
    condition_rules: List["ConditionRule"] = db.relationship("ConditionRule", back_populates="service",
                                                             cascade="all, delete")
    script_rules: List["ScriptRule"] = db.relationship("ScriptRule", back_populates="service", cascade="all, delete")

    def update(self, service):
        for col_name in self.__table__.columns.keys():
            if getattr(service, col_name):
                setattr(self, col_name, getattr(service, col_name))

    @staticmethod
    def find(name):
        service = db.session.query(Service).filter(Service.name == name).one_or_none()
        if service is None:
            raise NotFound("Не удалось найти сервис с таким именем")
        return service

    @staticmethod
    def exists(name):
        return db.session.query(exists().where(Service.name == name)).scalar()


class ConditionRule(db.Model):
    __tablename__ = "condition_rules"

    id = db.Column(db.Integer, primary_key=True)
    service_name = db.Column(db.String, db.ForeignKey('services.name'))
    service: Service = db.relationship("Service", back_populates="condition_rules")

    order = db.Column(db.Integer)
    protocol = db.Column(db.String, nullable=False)
    enabled = db.Column(db.Boolean, default=False)
    boolean_operator = db.Column(db.Enum(BooleanOperator), nullable=True)
    match_type = db.Column(db.String, nullable=False)
    match_relationship = db.Column(db.String, nullable=False)
    match_condition = db.Column(db.String, nullable=False)
    match_side = db.Column(db.String, nullable=False)
    action_type: ActionType = db.Column(db.Enum(ActionType), nullable=False)


class ScriptRule(db.Model):
    __tablename__ = "script_rules"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    service_name = db.Column(db.String, db.ForeignKey('services.name'))
    service: Service = db.relationship("Service", back_populates="script_rules")

    order = db.Column(db.Integer)
    enabled = db.Column(db.Boolean)
    protocol = db.Column(db.String, nullable=False)
    script = db.Column(db.String, nullable=False)
    boolean_operator = db.Column(db.Enum(BooleanOperator), nullable=True)
    action_type: ActionType = db.Column(db.Enum(ActionType), nullable=False)
