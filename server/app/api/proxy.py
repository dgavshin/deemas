from http import HTTPStatus

from flask_restx import Resource

from server.app import services_ns, proxy_ns
from server.app.errorhandler import ResponseEntity
from server.app.proxyhandler import *
from server.app.swagger import status_swag


@proxy_ns.route("/<string:name>")
@proxy_ns.param('name', 'Название сервиса')
class ProxyService(Resource):
    @services_ns.response(200, 'OK', model=status_swag)
    def get(self, name: str):
        """Возвращает статус прокси сервиса, true - прокси запущен"""
        return {"status": is_proxy_enabled(Service.find(name))}

    @services_ns.response(200, 'OK')
    def delete(self, name: str):
        """Останавливает прокси для указанного сервиса"""
        stop_proxy(Service.find(name))
        return ResponseEntity(HTTPStatus.OK, "Прокси успешно остановлен")

    @services_ns.response(200, 'OK')
    def post(self, name: str):
        """Создает прокси для указанного сервиса"""
        start_proxy(Service.find(name))
        return ResponseEntity(HTTPStatus.OK, "Прокси успешно создан")

    @services_ns.response(200, 'OK')
    def put(self, name: str):
        """Перезапускает прокси указанного сервиса"""
        restart_proxy(Service.find(name))
        return ResponseEntity(HTTPStatus.OK, "Прокси успешно перезагружен")