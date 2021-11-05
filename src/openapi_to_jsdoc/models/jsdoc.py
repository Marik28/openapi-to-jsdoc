from typing import Optional

from pydantic import BaseModel


class TypeProperty(BaseModel):
    name: str
    type: str
    description: Optional[str]
    required: bool = False


class JSDocTypeDefinition(BaseModel):
    type: str
    name: str
    description: Optional[str]
    properties: Optional[list[TypeProperty]]
