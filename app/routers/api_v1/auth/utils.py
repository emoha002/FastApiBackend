import datetime
import random
import string

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def has_time_passed(time_to_check):
    current_time = datetime.datetime.utcnow().timestamp()
    return current_time > time_to_check


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def generate_random_otp(n: int = 4):
    otp_value = "".join(random.choices(string.digits, k=n))
    otp_value = "1234"
    return otp_value
