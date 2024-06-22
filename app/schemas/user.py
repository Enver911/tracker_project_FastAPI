from pydantic import BaseModel, Field, EmailStr

class UserSchemaPasswordReset(BaseModel):
    email: EmailStr = Field(max_length=30)
    
class UserSchemaLogin(BaseModel):
    username: str = Field(max_length=30)
    password: str = Field(max_length=30)
    
class UserSchemaCreate(UserSchemaLogin):
    email: EmailStr = Field(max_length=30)
    
class UserSchemaPublicInfo(BaseModel):
    username: str = Field(max_length=30)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)
    avatar: str | None = Field(max_length=100, default=None)

class UserSchemaUpdate(BaseModel):
    username: str | None = Field(max_length=30, default=None)
    email: EmailStr | None = Field(max_length=30, default=None)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)

class UserSchemaRead(UserSchemaPublicInfo):
    id: int
    email: EmailStr = Field(max_length=30)