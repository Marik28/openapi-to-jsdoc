from pathlib import Path

import typer

from .services.generating import generate_jsdoc
from .services.parsing import parse_openapi_file
from .validators import validate_json_file

app = typer.Typer()


@app.command()
def main(
        openapi_file: Path = typer.Argument(
            ...,
            exists=True,
            file_okay=True,
            readable=True,
            resolve_path=True,
            callback=validate_json_file,
            help="File with openapi schema with json extension"
        ),
        encoding: str = typer.Option(
            "utf-8",
            "--encoding",
            "-e"
        ),
        output_dir_path: Path = typer.Option(
            Path.cwd(),
            "--output-path",
            "-o",
            resolve_path=True,
            show_default=False,
            help="Path where the generated file will be saved to."
                 " By default, a directory, from which the script was called",
        ),
        generated_file_name: str = typer.Option(
            "docs",
            help="javascript file name (without extension), in which the docs will be generated."
        ),
):
    """Generates javascript file with typedefs in JSDoc format, based on OpenAPI schemas"""
    js_filename = generated_file_name + ".js"
    output_file_path = output_dir_path / js_filename
    openapi = parse_openapi_file(openapi_file, encoding)
    generate_jsdoc(openapi, output_file_path)
    typer.echo(f"File is successfully generated! Path - {output_file_path}")


if __name__ == '__main__':
    app()
