# todo добавить определение массивов типов (Array<smth>)
from pathlib import Path

from ..models.jsdoc import JSDocTypeDefinition, TypeProperty
from ..models.openapi import Openapi, Property, Schema, Type


def wrap_lines(lines: list[str]) -> list[str]:
    lines = [f" * {line}\n" for line in lines]
    lines.insert(0, "/**\n")
    lines.append(" */\n")
    return lines


def get_property_type(prop: Property):
    prop_type = prop.type
    if prop.ref is not None:
        ref = prop.ref
    elif prop.all_of is not None:
        try:
            assert len(prop.all_of) == 1
        except AssertionError:
            # todo think of better exception
            raise RuntimeError("More than 1 refs are not yet supported") from None
        ref = prop.all_of[0].ref
    else:
        ref = None

    if ref is not None:
        prop_type = ref.split("/")[-1]
    return prop_type


def get_property_doc(prop: TypeProperty) -> str:
    doc = f"@property {{{'?' if not prop.required else ''}{prop.type}}} {prop.name}"

    if prop.description:
        doc += f" - {prop.description}"
    return doc


def get_typedef_doc(typedef: JSDocTypeDefinition) -> list[str]:
    lines = [f"@typedef {{{typedef.type}}} {typedef.name}"]
    if typedef.description is not None:
        lines.append(f"{typedef.description}")

    props = typedef.properties
    if props is not None:
        for prop in props:
            line = get_property_doc(prop)
            lines.append(line)
    lines.append("")
    return lines


def write_docs(typedefs: list[JSDocTypeDefinition], destination_path: Path):
    integer_typedef = JSDocTypeDefinition(
        name="integer",
        type="number",
    )
    lines = get_typedef_doc(integer_typedef)
    for typedef in typedefs:
        typedef_lines = get_typedef_doc(typedef)
        lines.extend(typedef_lines)
    lines = wrap_lines(lines)

    with open(destination_path, "wt", encoding="utf-8") as f:
        f.writelines(lines)


def generate_jsdoc_for_schema(schema: Schema) -> JSDocTypeDefinition:
    typedef = JSDocTypeDefinition(
        description=schema.description,
        name=schema.title,
        type=schema.type,
    )

    if schema.type != Type.OBJECT.value:
        return typedef

    typedef.properties = []
    required_properties = schema.required if schema.required is not None else []
    for name, prop in schema.properties.items():
        required = name in required_properties
        prop_type = get_property_type(prop)

        generated_prop = TypeProperty(
            **{
                "name": name,
                "type": prop_type,
                "required": required,
                "description": prop.description,
            })
        typedef.properties.append(generated_prop)
    return typedef


def generate_jsdoc(openapi: Openapi, destination_path: Path):
    schemas = openapi.components.schemas
    jsdoc = [generate_jsdoc_for_schema(schema) for _, schema in schemas.items()]
    write_docs(jsdoc, destination_path)
