from flask import json

from server.app.errorhandler import ValidationError


def read_value(data, clazz):
    try:
        return json.loads(data, object_hook=lambda x: clazz(**x))
    except Exception:
        raise ValidationError(f"Не удалось преобразовать json к классу {clazz.__name__}")


def not_none(data, var_name="Входящий параметр"):
    if not data:
        raise ValidationError(f"{var_name} не может быть пустым")
    return data


def between(data: int, _min: int, _max: int, var_name="Входящий параметр"):
    if data < _min:
        raise ValidationError(f"{var_name} не может быть меньше {_min}")
    if data > _max:
        raise ValidationError(f"{var_name} не может быть больше {_max}")
    return data


def ipv4(address, var_name="Входящий параметр"):
    if not address.replace('.', '').isnumeric():
        raise ValidationError(f"{var_name} не является ipv4")
    return address


