from passlib.context import CryptContext
import configparser
from typing import Union, Any
import datetime
import jwt
from utils.constants import (
    REFRESH_TOKEN_EXPIRE_MINUTES,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    JWT_REFRESH_SECRET_KEY,
    JWT_SECRET_KEY,
    ALGORITHM,
)

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(password: str, hashed_pass: str):
    '''
    Verify Hashed Password
    @param password: Given Password (str)
    @param hashed_password: Hashed password in DB (str)
    @return True/False
    '''
    return password_context.verify(password, hashed_pass)


def create_access_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    '''
    Create new JWT access token
    @param subject: Subject used to create JWT (str)
    @param expires_delta: Expiry time (int)
    @return encoded_jwt: New JWT Token (str)
    '''
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: int = None
) -> str:
    '''
    Create new Refresh JWT access token
    @param subject: Subject used to create JWT (str)
    @param expires_delta: Expiry time (int)
    @return encoded_jwt: New JWT Token (str)
    '''
    if expires_delta is not None:
        expires_delta = datetime.datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.datetime.utcnow() + datetime.timedelta(
            minutes=REFRESH_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def read_config():
    '''
    Read configs
    '''
    config = configparser.ConfigParser()
    config.read('config.ini')

    config_dict = {}
    for section in config.sections():
        config_dict[section] = dict(config.items(section))

    return config_dict


