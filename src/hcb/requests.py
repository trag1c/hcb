from typing import Any, TypeVar, cast
from urllib.parse import urlencode

import httpx
from pydantic import TypeAdapter, ValidationError

T = TypeVar("T")
BASE_URL = "https://hcb.hackclub.com/api/v3"


class HCBAPIError(Exception):
    pass


def validate(obj: object, expected_type: type[T]) -> T:
    try:
        return TypeAdapter[T](expected_type).validate_python(obj)
    except ValidationError:
        if isinstance(obj, dict) and obj.keys() == {"message"}:
            # It's an HCB ErrorResponse object
            raise HCBAPIError(cast("dict[str, Any]", obj["message"])) from None
        raise


def req_url(path: str, query: dict[str, Any]) -> str:
    if not query:
        return BASE_URL + path
    params = urlencode({k: v for k, v in query.items() if v is not None})
    return BASE_URL + path + "?" + params


async def arequest(path: str, query: dict[str, Any], expected_type: type[T]) -> T:
    async with httpx.AsyncClient() as client:
        resp = await client.get(req_url(path, query))
    return validate(resp.json(), expected_type)


def request(path: str, query: dict[str, Any], expected_type: type[T]) -> T:
    return validate(httpx.get(req_url(path, query)).json(), expected_type)
