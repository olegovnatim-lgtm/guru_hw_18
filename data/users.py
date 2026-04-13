from dataclasses import dataclass
from enum import Enum


class Gender(str, Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"


class Hobbies(str, Enum):
    SPORTS = "Sports"
    READING = "Reading"
    MUSIC = "Music"


@dataclass
class User:
    first_name: str
    last_name: str
    email: str
    gender: Gender
    mobile: str
    year_of_birth: str
    month_of_birth: str
    day_of_birth: str
    subject: str
    hobbies: Hobbies
    picture: str
    address: str
    state: str
    city: str
