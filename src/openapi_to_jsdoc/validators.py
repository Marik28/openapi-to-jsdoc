from pathlib import Path

import typer


def validate_json_file(file: Path) -> Path:
    if not file.name.endswith(".json"):
        raise typer.BadParameter("Нужен .json файл")

    return file
