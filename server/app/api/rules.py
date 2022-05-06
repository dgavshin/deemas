from http import HTTPStatus

from flask import request, json
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest

from proxy.conditions import protocol_conditions
from server.app import conditions_ns, scripts_ns
from server.app import db, condition_rules_schema, script_rule_swag, response_swag, condition_rule_options_swag
from server.app import script_rules_schema
from server.app.errorhandler import ResponseEntity
from server.app.models import Service
from server.app.swagger import condition_rule_swag


def update_rules(service_name: str, data, schema):
    if not request.data:
        raise BadRequest("Пустой запрос")

    service = db.session.query(Service).filter(Service.name == service_name).one_or_none()
    if not service:
        raise NotFound(f"Не удалось найти сервис с именем {service_name}")
    rules = schema.loads(data)
    for rule in rules:
        rule.protocol = service.protocol
    return service, rules


@conditions_ns.route("/<string:service_name>")
@conditions_ns.response(404, 'Сервис с указанным именем не найден', model=response_swag)
@conditions_ns.response(400, 'Ошибка клиента', model=response_swag)
@conditions_ns.param('service_name', 'Название сервиса')
class ConditionRulesResource(Resource):

    @conditions_ns.doc('read_condition_rule')
    @conditions_ns.marshal_list_with(condition_rule_swag)
    def get(self, service_name):
        """Выводит список правил указанного сервиса"""
        service = db.session.query(Service) \
            .filter(Service.name == service_name) \
            .one_or_none()
        if service:
            return json.loads(condition_rules_schema.dumps(service.condition_rules))
        raise NotFound(f"Не удалось найти сервис с именем {service_name}")

    @conditions_ns.doc('update_service')
    @conditions_ns.expect([condition_rule_swag])
    @conditions_ns.response(201, 'Правила успешно обновлены', model=response_swag)
    def put(self, service_name):
        """Переписывает список правил указанного сервиса"""
        service, rules = update_rules(service_name, request.data, condition_rules_schema)
        service.condition_rules = rules
        db.session.add(service)
        db.session.commit()
        return ResponseEntity(HTTPStatus.CREATED, f"Condition правила для сервиса {service_name} успешно обновлены")


@scripts_ns.route("/<string:service_name>")
@scripts_ns.response(404, 'Сервис с указанным именем не найден', model=response_swag)
@conditions_ns.response(400, 'Ошибка клиента', model=response_swag)
@scripts_ns.param('service_name', 'Название сервиса')
class ScriptRulesResource(Resource):

    @scripts_ns.doc('read_script_rule')
    @scripts_ns.marshal_list_with(script_rule_swag)
    def get(self, service_name):
        """Выводит список правила указанного сервиса"""
        service = db.session.query(Service) \
            .filter(Service.name == service_name) \
            .one_or_none()
        if service:
            return json.loads(script_rules_schema.dumps(service.script_rules))
        raise NotFound(f"Не удалось найти сервис с именем {service_name}")

    @scripts_ns.doc('update_script_rules')
    @scripts_ns.expect([script_rule_swag])
    @conditions_ns.response(201, 'Правила успешно обновлены', model=response_swag)
    def put(self, service_name):
        """Переписывает список script правил указанного сервиса"""
        service, rules = update_rules(service_name, request.data, script_rules_schema)
        service.script_rules = rules
        db.session.add(service)
        db.session.commit()
        return ResponseEntity(HTTPStatus.CREATED, f"Script правила для сервиса {service_name} успешно обновлены")


@conditions_ns.route('/options/<string:protocol>')
@conditions_ns.response(404, 'Не найдено опций для указанного протокола', model=response_swag)
@conditions_ns.response(400, 'Ошибка клиента', model=response_swag)
class ConditionRuleUtils(Resource):

    @scripts_ns.doc('get_condition_options')
    @scripts_ns.marshal_list_with(condition_rule_options_swag)
    @conditions_ns.response(201, 'Правила успешно обновлены', model=response_swag)
    def get(self, protocol: str):
        """Возвращает список доступных опций для создания правил"""
        cond = protocol_conditions.get(protocol.lower())
        if cond is None:
            raise NotFound(f"Не удалось найти условия для протокола {protocol}")
        return [cond[x].serialize(x) for x in cond.keys()]

