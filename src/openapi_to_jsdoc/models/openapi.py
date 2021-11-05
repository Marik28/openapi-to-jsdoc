import enum
from typing import Optional

from pydantic import BaseModel, Field


class OpenapiInfo(BaseModel):
    title: str
    version: str


class Ref(BaseModel):
    ref: str = Field(..., alias="$ref")


class Property(BaseModel):
    ref: Optional[str] = Field(None, alias="$ref")
    all_of: Optional[list[Ref]] = Field(None, alias="allOf")
    title: Optional[str]
    type: Optional[str]
    format: Optional[str]
    description: Optional[str]
    enum: Optional[list[str]]


class Type(enum.Enum):
    OBJECT = "object"
    NUMBER = "number"
    INTEGER = "integer"
    BOOLEAN = "boolean"
    STRING = "string"


class Schema(BaseModel):
    title: str
    description: Optional[str]
    required: Optional[list[str]]
    type: str
    properties: Optional[dict[str, Property]]


class Components(BaseModel):
    schemas: dict[str, Schema]


class Openapi(BaseModel):
    openapi: str
    info: OpenapiInfo
    components: Components

