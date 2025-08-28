from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Any
from datetime import datetime
from bson import ObjectId # type: ignore

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, handler=None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema: dict[str, Any], handler) -> dict[str, Any]:
        field_schema.update(type="string")
        return field_schema

class User(BaseModel):
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str}
    )
    
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: str
    hashed_password: str
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class UserInDB(BaseModel):
    id: str
    username: str
    email: str
    hashed_password: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None