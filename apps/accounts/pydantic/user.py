


from pydantic import BaseModel, EmailStr


class UserInfoPydantic(BaseModel):
    email: EmailStr
    is_super: bool
    list_permission: list[str]
    list_role_code: list[str]