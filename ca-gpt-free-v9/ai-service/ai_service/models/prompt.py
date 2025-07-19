from typing import Optional
from beanie import Document, PydanticObjectId
from pydantic import Field

class Prompt(Document):
    name: str
    text: str
    companyId: Optional[PydanticObjectId] = Field(default=None, index=True)

    class Settings:
        name = "prompts"
        indexes = [
            [("name", 1), ("companyId", 1), {"unique": True}]
        ]
