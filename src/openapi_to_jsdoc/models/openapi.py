import enum
from typing import Optional, Union

from pydantic import BaseModel, Field, validator


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


class Components(BaseModel):
    schemas: dict[str, Schema]


class Openapi(BaseModel):
    openapi: str
    info: OpenapiInfo
    components: Components
