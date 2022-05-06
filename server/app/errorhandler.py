import traceback

from flask import Response, json
from werkzeug.exceptions import HTTPException

from server.app import api


class ValidationError(Exception):
    def __init__(self, description):
        self.description = description


class ResponseEntity(Response):
    def __init__(self, code, description, level: str = "info"):
        super().__init__()
        self.data = json.dumps({"code": code, "description": description, "level": level})
        self.status = code
        self.mimetype = 'application/json'


def handle_http_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    return ResponseEntity(e.code, e.description, level="error")


@api.errorhandler(Exception)
def handle_exception(e: Exception):
    traceback.print_exc()
    code = e.code if isinstance(e, HTTPException) else 500
    return {"code": code, "description": getattr(e, 'description', str(e)), "level": "error"}, code
