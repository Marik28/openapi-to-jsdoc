from json import JSONDecodeError
from pathlib import Path

import typer
from pydantic import ValidationError

from ..models.openapi import Openapi


def parse_openapi_file(file: Path, encoding) -> Openapi:
    try:
        openapi = Openapi.parse_file(file, encoding=encoding)
    except ValidationError as e:
        raise typer.BadParameter(f"Ошибка парсинга json: {e.json()}")
    except JSONDecodeError as e:
        raise typer.BadParameter(f"Ошибка декодирования файла: {e.args}")
    return openapi
