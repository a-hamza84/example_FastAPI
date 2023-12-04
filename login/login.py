from sqlalchemy import select
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from models.base import SESSION
from models.users import User

from utils.helpers import (
    verify_password,
    create_access_token,
    create_refresh_token,
)

router = APIRouter()


def get_user(email, password):
    '''
    Query user from database
    @param email: Email address
    @param password: Password
    @return User object else Nones
    '''
    stmt = select(User).where(User.email == email, User.password == password)
    obj = SESSION.execute(stmt).fetchall()
    for row in obj:
        return dict(row)
    return None


@router.post('/login')
def login(item: dict):
    '''
    Login Endpoint
    '''
    if 'email' not in item or 'password' not in item:
        return JSONResponse(
            status_code=400, content={"error": "Invalid input params"}
        )
    user = get_user(item['email'], item['password'])
    if user is None:
        return JSONResponse(
            status_code=400, content={"error": "Invalid Email or Password"}
        )
    hashed_pass = user['password']
    if not verify_password(item['password'], hashed_pass):
        return JSONResponse(
            status_code=400, content={"error": "Invalid Password"}
        )
    return JSONResponse(
        content={
            "message": "Login Success",
            "access_token": create_access_token(item['email']),
            "refresh_token": create_refresh_token(item['email']),
        }
    )


@router.post('/signup')
def login(item: dict):
    '''
    Signup Endpoint
    '''
    if 'email' not in item or 'password' not in item:
        return JSONResponse(
            status_code=400, content={"error": "Invalid input params"}
        )
    user_obj = User(item['username'], item['password'], item['email'])
    user_obj.save_user()
    return JSONResponse(
        content={
            "message": "Signup Success",
        }
    )
