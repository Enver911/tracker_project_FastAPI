from pydantic import BaseModel, Field, EmailStr


class UserSchemaLogin(BaseModel):
    username: str | None = Field(max_length=30, default=None)
    password: str | None = Field(max_length=30, default=None)
    
class UserSchemaCreate(UserSchemaLogin):
    email: EmailStr | None = Field(max_length=30, default=None)


class UserSchemaUpdate(BaseModel):
    username: str | None = Field(max_length=30, default=None)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)
    password: str | None = Field(max_length=30, default=None)
    password2: str | None = Field(max_length=30, default=None) 

class UserSchemaRead(BaseModel):
    email: EmailStr | None = Field(max_length=30, default=None)
    username: str | None = Field(max_length=30, default=None)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)