from pydantic import BaseModel


class Dog(BaseModel):
    id: str
    user_id: str
    dog_name: str
    picture: str
    create_date: str
    is_adopted: bool


class User(BaseModel):
    user_id: str
    user_name: str
    last_name: str
    email: str


class Admin_Login(BaseModel):
    username: str
    password: str

