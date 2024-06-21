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

class UserSchemaUpdate(BaseModel):
    username: str | None = Field(max_length=30, default=None)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)
    password: str | None = Field(max_length=30, default=None)
    password2: str | None = Field(max_length=30, default=None) 

class UserSchemaRead(BaseModel):
    email: EmailStr = Field(max_length=30)
    username: str = Field(max_length=30)
    avatar: str | None = Field(max_length=100, default=None)
    firstname: str | None = Field(max_length=30, default=None)
    lastname: str | None = Field(max_length=30, default=None)
    
class JWT(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    
    