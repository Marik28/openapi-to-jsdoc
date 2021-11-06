import enum
from typing import Optional, Union

from pydantic import BaseModel, Field, validator


def to_lower_camel_case(word: str) -> str:
    parts = []
    for index, part in enumerate(word.split("_")):
        if index == 0:
            parts.append(part.lower())
        else:
            parts.append(part.capitalize())
    return "".join(parts)


class OpenapiInfo(BaseModel):
    title: str
    version: str


class Ref(BaseModel):
    ref: str = Field(..., alias="$ref")


class ArrayType(BaseModel):
    type: str

    @validator("type")
    def capitalize_type(cls, value: Optional[str]):
        if value is None:
            return None
        return value.capitalize()


class Property(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    all_of: Optional[list[Ref]] = Field(None, alias="allOf")
    title: Optional[str]
    type: Optional[str]
    format: Optional[str]
    description: Optional[str]
    enum: Optional[list[str]]
    items: Optional[Union[Ref, ArrayType]]

    @validator("type")
    def capitalize_type(cls, value: Optional[str]):
        if value is None:
            return None
        return value.capitalize()


class Type(enum.Enum):
    OBJECT = "object"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    STRING = "string"
    ARRAY = "array"


class Schema(BaseModel):
    title: str
    description: Optional[str]
    required: Optional[list[str]]
    type: str
    properties: Optional[dict[str, Property]]

    @validator("type")
    def capitalize_type(cls, value: Optional[str]):
        if value is None:
            return None
        return value.capitalize()

    @validator("properties")
    def props_to_lower_camel_case(cls, props: dict):
        props = {to_lower_camel_case(prop_name): prop_value for prop_name, prop_value in props.items()}
        return props


class Components(BaseModel):
    schemas: dict[str, Schema]


class Openapi(BaseModel):
    openapi: str
    info: OpenapiInfo
    components: Components
