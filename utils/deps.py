from fastapi import Depends
import jwt
from utils.constants import JWT_SECRET_KEY, ALGORITHM
from fastapi.security import OAuth2PasswordBearer
import datetime
from pydantic import ValidationError
import traceback

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def check_jwt(token: str = Depends(oauth2_scheme)):
    '''
    Verify JWT Token
    @param token: JWT (str)
    @return True/False
    '''
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        if (
            datetime.datetime.fromtimestamp(payload['exp'])
            < datetime.datetime.now()
        ):
            return False
    except (jwt.JWTError, ValidationError) as exce:
        print(exce)
        traceback.print_exc()
        return False
    return True
