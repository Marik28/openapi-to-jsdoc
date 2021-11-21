from pathlib import Path
from typing import Optional

from ..models.jsdoc import JSDocTypeDefinition, TypeProperty
from ..models.openapi import Openapi, Property, Schema, Ref


def wrap_lines(lines: list[str]) -> list[str]:
    lines = [f" * {line}\n" for line in lines]
    lines.insert(0, "/**\n")
    lines.append(" */\n")
    return lines


def get_items_type(prop: Property) -> Optional[str]:
    if prop.items is None:
        return None

    if isinstance(prop.items, Ref):
        items_type = prop.items.ref.split("/")[-1]
    else:
        items_type = prop.items.type

    return items_type


def get_property_type(prop: Property) -> tuple[str, Optional[str]]:
    """
    :return: -> (property_type, items). If property_type is Array, items is type of objects in array, otherwise - None.
    """
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

    items = get_items_type(prop)
    return prop_type, items


def wrap_type(items: Optional[str]) -> str:
    if items is None:
        return ""
    return f"<{items}>"


def get_property_doc(prop: TypeProperty) -> str:
    items = prop.items
    doc = f"@property {{{'?' if not prop.required else ''}{prop.type}{wrap_type(items)}}} {prop.name}"

    title = f"{prop.title}" if prop.title is not None else ""
    description = prop.description if prop.description is not None else ""
    if description or title:
        doc += f" - {title.strip()}{'.' if description else ''} {description.strip()}".rstrip()
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
        name="Integer",
        type="Number",
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

    if schema.type != "Object":
        return typedef

    typedef.properties = []
    required_properties: list[str] = schema.required if schema.required is not None else []
    for name, prop in schema.properties.items():
        required = name in required_properties
        prop_type, items = get_property_type(prop)
        title = prop.title
        generated_prop = TypeProperty(
            name=name,
            type=prop_type,
            items=items,
            title=title,
            description=prop.description,
            required=required,
        )
        typedef.properties.append(generated_prop)
    return typedef


def generate_jsdoc(openapi: Openapi, destination_path: Path):
    schemas = openapi.components.schemas
    jsdoc = [generate_jsdoc_for_schema(schema) for _, schema in schemas.items()]
    write_docs(jsdoc, destination_path)
