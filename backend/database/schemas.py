from pydantic import BaseModel


class FeedBase(BaseModel):
    title: str
    url: str
    description: str | None = None


class FeedCreate(FeedBase):
    pass


class Feed(FeedBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    full_name: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    feeds: list[Feed] = []

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None