# -*- coding: utf-8 -*-
import json

__all__ = ["get_body", "get_status_code", "get_query_parameters"]

import uuid
from datetime import datetime
from typing import Union
from decimal import Decimal


def get_body(event: dict):
    """
    Get event body if lambda has proxy lambda integration in api_local gateway.
    Parameters
    ----------
    event : dict

    Returns
    -------
    dict
        dictionary with body information.

    Examples
    --------
    >>> from core_api.utils import get_body
    >>> get_body({"body": {"a": 1}})

    """
    if isinstance(event, str):
        event = json.loads(event)
    body = event.get("body")
    if isinstance(body, str):
        return json.loads(body)
    return body


def get_status_code(response):
    """
    Get a status code from the lambda response if you use the decorator LambdaResponseWebDefault.
    Parameters
    ----------
    response : dict
        lambda response in api format.

    Returns
    -------
    int
        Status code returned.

    Examples
    --------
    >>> from core_api.utils import get_status_code
    >>> get_status_code({"statusCode": 200})

    """
    status_code = response.get("statusCode")
    return status_code


def get_query_parameters(event: Union[str, dict]):
    """
    Get event query parameters if lambda has proxy lambda integration in api_local gateway.
    Parameters
    ----------
    event : dict

    Returns
    -------
    dict
        dictionary with query parameters if exists.

    Examples
    --------
    >>> from core_api.utils import get_query_parameters
    >>> get_query_parameters({"queryStringParameters": {"a": 1}})

    """
    if isinstance(event, str):
        events = json.loads(event)
        return events.get("queryStringParameters") or {}
    return event.get("queryStringParameters") or {}


def is_valid_uuid(value):
    """
    Validation uuid
    Args:
        event:

    Returns: bool

    """
    try:
        uuid.UUID(value)
        return True
    except ValueError:
        return False


def get_path_parameters(event: Union[str, dict]):
    """
    Get event path parameters if lambda has proxy lambda integration in api_local gateway.
    Parameters
    ----------
    event : dict

    Returns
    -------
    dict
        dictionary with path parameters if exists.

    Examples
    --------
    >>> from core_api.utils import get_path_parameters
    >>> get_path_parameters({"pathParameters": {"a": 1}})

    """
    if isinstance(event, str):
        events = json.loads(event)
        return events.get("pathParameters") or {}
    return event.get("pathParameters") or {}


def cast_date(element: Union[datetime.date, datetime.time]):
    """
    Cast a datetime.date or datetime.time object to iso-format string.

    Parameters
    ----------
    element: datetime.date or datetime.time object

    Returns
    -------
    str: iso-format string

    Examples
    --------
    >>> from core_api.utils import cast_date
    >>> cast_date(datetime.date(2020, 1, 1))

    """
    if isinstance(element, (datetime.date, datetime.time)):
        element_ = element.isoformat()
        return element_


def cast_number(number: Union[str, Decimal]) -> float | int | None:
    """
    Cast a string or Decimal object to int or float.

    Parameters
    ----------
    number : str or Decimal

    Returns
    -------
    int or float

    Examples
    --------
    >>> from core_api.utils import cast_number
    >>> cast_number(Decimal(1.1))

    """
    if isinstance(number, str):
        if number.isnumeric():
            return int(number)
        else:
            try:
                return float(number)
            except ValueError:
                try:
                    return float(number.replace(",", ""))
                except ValueError:
                    raise ValueError("The value not is int o float")
    elif isinstance(number, Decimal):
        return cast_number(str(number))
    elif isinstance(number, (float, int)):
        return number


def cast_default(o):
    """
    Cast data to default data for json serialization.

    Parameters
    ----------
    o : Any

    Returns
    -------
    Any object with the default data type for json serialization.

    Examples
    --------
    >>> from core_api.utils import cast_default
    >>> cast_default(Decimal(1.1))

    """
    o = cast_date(o)
    if isinstance(o, Decimal):
        o = cast_number(o)
    return o
