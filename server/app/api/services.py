from http import HTTPStatus

from flask import request, json
from flask_restx import Resource
from werkzeug.exceptions import NotFound, BadRequest
from server.app.api.rules import add_default_script_rules

from server.app import db, services_schema, service_schema, services_ns
from server.app.errorhandler import ResponseEntity
from server.app.proxyhandler import *
from server.app.swagger import service_swag_create, response_swag, service_swag_update, service_swag_read


@services_ns.route("/")
@services_ns.response(400, 'Ошибка клиента', model=response_swag)
@services_ns.response(200, 'OK', model=response_swag)
class ServiceListResource(Resource):
    """Shows a list of all todos, and lets you POST to add new tasks"""

    @services_ns.doc('list_services')
    @services_ns.marshal_list_with(service_swag_read)
    def get(self):
        """Выводит список всех сервисов"""
        all_services = db.session.query(Service).all()
        return json.loads(services_schema.dumps(all_services))

    @services_ns.doc('create_service')
    @services_ns.expect(service_swag_create)
    @services_ns.response(201, 'Сервис успешно создан', model=response_swag)
    def post(self):
        """Создает новый сервис"""
        if Service.exists(request.json["name"]):
            raise BadRequest(f"Сервис с таким именем уже создан")

        service = service_schema.loads(request.data)
        add_default_script_rules(service)
        db.session.add(service)
        db.session.commit()
        return ResponseEntity(HTTPStatus.CREATED, f"Сервис {service.name} успешно создан")


@services_ns.route("/<string:name>")
@services_ns.response(404, 'Сервис с указанным именем не найден', model=response_swag)
@services_ns.response(400, 'Ошибка клиента', model=response_swag)
@services_ns.response(200, 'OK', model=response_swag)
@services_ns.param('name', 'Название сервиса')
class ServiceResource(Resource):

    @services_ns.doc('read_service')
    @services_ns.marshal_with(service_swag_read)
    def get(self, name):
        """Возвращает сервис по имени"""
        return Service.find(name)

    @services_ns.doc('update_service')
    @services_ns.response(201, 'Сервис обновлен', model=response_swag)
    @services_ns.expect(service_swag_update)
    def put(self, name):
        """Обновляет сервис по имени"""
        Service.find(name).update(service_schema.loads(request.data))
        db.session.commit()
        return ResponseEntity(HTTPStatus.CREATED, f"Сервис {name} успешно обновлен")

    @services_ns.response(200, 'Сервис удален', model=response_swag)
    @services_ns.doc('delete_service')
    def delete(self, name):
        """Удаляет сервис по имени и останавливает его"""
        service = db.session.query(Service).filter(Service.name == name).one_or_none()
        if not service:
            raise NotFound(f"Сервиса с именем {name} не существует")
        db.session.delete(service)
        db.session.commit()
        return ResponseEntity(HTTPStatus.CREATED, f"Сервис {name} успешно удален")
