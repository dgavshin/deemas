from http import HTTPStatus

from flask_restx import Resource

from server.app import services_ns, iptables_ns
from server.app.errorhandler import ResponseEntity
from server.app.iptcmanager import *
from server.app.proxyhandler import is_proxy_enabled
from server.app.swagger import status_swag


@iptables_ns.route("/<string:name>")
@iptables_ns.param('name', 'Название сервиса')
class ProxyService(Resource):
    @services_ns.response(200, 'OK', model=status_swag)
    def get(self, name: str):
        """Возвращает true, если редирект включен, иначе false"""
        return {"status": is_redirect_enabled(Service.find(name))}

    @services_ns.response(200, 'OK')
    def delete(self, name: str):
        """Удаляет правило редиректа для указанного сервиса"""
        delete_redirect_rule(Service.find(name))
        return ResponseEntity(HTTPStatus.OK, "Redirect правило успешно удалено")

    @services_ns.response(200, 'OK')
    def post(self, name: str):
        """Создает правило редиректа для сервиса"""
        service = Service.find(name)
        if not is_proxy_enabled(service):
            raise ValueError("Нельзя создать redirect правило, если proxy для сервиса не работает")
        insert_redirect_rule(Service.find(name))
        return ResponseEntity(HTTPStatus.OK, "Redirect правило успешно добавлено")
