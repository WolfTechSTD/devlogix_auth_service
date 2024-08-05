from dataclasses import dataclass


@dataclass
class UserDTO:
    id: str
    username: str
    email: str


@dataclass
class CreateUserDTO:
    username: str
    email: str
    password: str
