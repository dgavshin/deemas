from flask_restx import fields

from server.app import restx

service_swag_read = restx.model('ServiceResponse', {
    'name': fields.String(required=True, description='Название сервиса'),
    'lang': fields.String(required=True, description='Язык программирования сервиса'),
    'port': fields.Integer(required=True, description='Порт прокси'),
    'proxy_port': fields.Integer(required=True, description='Порт куда проксить'),
    'proxy_host': fields.String(required=True, description='Хост куда проксить'),
    'protocol': fields.String(enum=["HTTP", "TCP"], required=True, description='Протокол сервиса'),
    'rule_operator': fields.String(enum=["AND", "OR"], required=True,
                                   description='Булевый оператор между скриптовыми и условными правилами')
})

service_swag_create = restx.model('CreateServiceRequest', {
    'name': fields.String(required=True, description='Название сервиса'),
    'lang': fields.String(required=True, description='Язык программирования сервиса'),
    'port': fields.Integer(required=True, description='Порт сервиса'),
    'proxy_port': fields.Integer(required=True, description='Прокси порт сервиса'),
    'proxy_host': fields.String(required=True, description='Прокси хост сервиса'),
    'protocol': fields.String(enum=["HTTP", "TCP"], required=True, description='Протокол сервиса'),
    'rule_operator': fields.String(enum=["AND", "OR"], required=True,
                                   description='Булевый оператор между скриптовыми и условными правилами')
})

service_swag_update = restx.model('UpdateServiceRequest', {
    'lang': fields.String(required=True, description='Язык программирования сервиса'),
    'port': fields.Integer(required=True, description='Порт сервиса'),
    'proxy_port': fields.Integer(required=True, description='Прокси порт сервиса'),
    'proxy_host': fields.String(required=True, description='Прокси хост сервиса'),
    'protocol': fields.String(enum=["HTTP", "TCP"], required=True, description='Протокол сервиса'),
    'rule_operator': fields.String(enum=["AND", "OR"], required=True,
                                   description='Булевый оператор между скриптовыми и условными правилами')
})

condition_rule_swag = restx.model("ConditionRule", {
    "id": fields.Integer(required=False, description="Идентификатор правила"),
    "order": fields.Integer(required=True, description="Порядок правила"),
    "enabled": fields.Boolean(required=True, description="Включено ли правило"),
    "boolean_operator": fields.String(enum=["AND", "OR"], required=True, description="Булевый оператор правила"),
    "match_type": fields.String(required=True, description="Место поиска совпадений"),
    "match_relationship": fields.String(required=True, description="Действие при поиске совпадения"),
    "match_condition": fields.String(required=True, description="Условие совпадения"),
    "match_side": fields.String(required=True, description="Сторона совпадения"),
    "action_type": fields.String(enum=["ENCRYPT", "DECRYPT"], required=True, description="Тип действия")
})

script_rule_swag = restx.model("ScriptRule", {
    "name": fields.String(required=True, description="Идентификатор правила"),
    "order": fields.Integer(required=True, description="Порядок правила"),
    "enabled": fields.Boolean(required=True, description="Включено ли правило"),
    "boolean_operator": fields.String(enum=["AND", "OR"], required=True, description="Булевый оператор правила"),
    "script": fields.String(required=True, description="Python скрипт с логикой правила"),
    "action_type": fields.String(enum=["ENCRYPT", "DECRYPT"], required=True, description="Тип действия")
})

response_swag = restx.model("ResponseEntity", {
    "code": fields.String(description="Код ответа"),
    "description": fields.String(description="Описание ответа"),
    "level": fields.String(enum=["info", "error", "warn"], description="Уровень логирования")
})

status_swag = restx.model("Status", {
    "enabled": fields.Boolean(description="Статус")
})

condition_rule_options_swag = restx.model("ConditionOptions", {
    "match_type": fields.String(description="Название поля для сравнения"),
    "match_relationships": fields.List(fields.String, description="Возможные типы сравнений между объектами"),
    "match_sides": fields.List(fields.String, description="Контекст для сравнения")
})
