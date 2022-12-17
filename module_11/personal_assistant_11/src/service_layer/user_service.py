from src.service_layer.unit_of_work import AbstractUnitOfWork
from src.domain.user_model import User
import bcrypt
from flask import session
from datetime import datetime, timedelta
import uuid


def create(username: str, email: str, password: str, uow: AbstractUnitOfWork):
    with uow:
        p_hash = bcrypt.hashpw(password.encode(
            "utf-8"), bcrypt.gensalt(rounds=10))
        user = User(username, email, p_hash)
        uow.users.add(user)
        uow.commit()
    return user


def login(email, password, uow: AbstractUnitOfWork) -> bool:
    with uow:
        user = uow.users.find_by_email(email)
        if not user:
            return False
        if not bcrypt.checkpw(password.encode('utf-8'), user.p_hash):
            return False
        session['username'] = {'username': user.username, 'id': user.id}
    return True


def loggin_user_if_can(token, uow: AbstractUnitOfWork):
    with uow:
        user = uow.users.get_by_token(token)
        if user:
            session['username'] = {'username': user.username, 'id': user.id}


def remember_current_user(uow: AbstractUnitOfWork):
    with uow:
        user_id = session['username']['id']
        user = uow.users.get(user_id)
        token = str(uuid.uuid4())
        user.token_cookie = token
        uow.commit()
    expired_date = datetime.now() + timedelta(days=60)
    return (token, expired_date)
