from dataclasses import dataclass


@dataclass
class UserView:
    id: str
    username: str
    email: str


@dataclass
class CreateUserView:
    username: str
    email: str
    password: str
