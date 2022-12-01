from __future__ import annotations

import inspect
import json
from typing import Any, Optional, Protocol, Union, runtime_checkable

Literal = Union[int, float, str, bytes, bool, None]
Array = list["JSON"]
Object = dict[str, "JSON"]
Container = Union[Array, Object]
JSON = Union[Literal, Array, Object]

JSONLiteral = Literal
JSONArray = Array
JSONObject = Object
JSONContainer = Container
JSONType = JSON

NoneType = type(None)
Literals = (int, float, str, bytes, bool, NoneType)
JSONTuple = ()


def is_encodable(object_: Any) -> bool:
    if isinstance(object_, Literals):
        return True
    elif isinstance(object_, list):
        return all(is_encodable(o) for o in object_)
    elif isinstance(object_, dict):
        return all(isinstance(key, str) and is_encodable(value) for key, value in object_.items())
    return False


@runtime_checkable
class JSONEncodable(Protocol):
    def __json__(self, *args: ..., **kwargs: ...) -> JSON:
        """Returns an object normally serializable by the standard library `json` module"""


def make_encodable(object_: Any, *args: ..., **kwargs: ...) -> JSON:
    if isinstance(object_, Literals):
        return object_
    elif isinstance(object_, JSONEncodable):
        object_ = object_.__json__(*args, **kwargs)

    if isinstance(object_, list):
        return [make_encodable(o) for o in object_]
    elif isinstance(object_, dict):
        return {str(make_encodable(key)): make_encodable(value) for key, value in object_.items()}

    raise RuntimeError(f"Can't encode object of type {type(object_)}")


def encode(object_: Any, **kwargs: ...) -> str:
    encodable: JSON = make_encodable(object_)
    return json.dumps(encodable, **kwargs)

def encode_as_dict(object_: Any, **kwargs) -> Object:
    
