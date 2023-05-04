
import secrets
from database import *
from routes.common import *
from argon2 import PasswordHasher
from functools import wraps


ag2 = PasswordHasher()


def generate_token_for_account(account: Account) -> None:
    token_data = secrets.token_urlsafe(64)
    token = SessionToken(
        account_id=account.id,
        token=token_data,
        max_age=int(time.time()) + 2592000  # 1 month
    )
    dbsession.add(token)
    dbsession.commit()
    session['secret'] = token_data


def get_account_from_session() -> Account:
    if 'secret' not in session:
        return None
    token = dbsession.query(SessionToken).filter(SessionToken.token == session['secret']).first()
    if not token:
        return None
    if int(time.time()) > token.max_age:
        dbsession.delete(token)
        dbsession.commit()
    return token.account


def clear_session() -> None:
    if not get_account_from_session():
        return
    token = dbsession.query(SessionToken).filter(
        SessionToken.token == session['secret']).first()
    dbsession.delete(token)
    dbsession.commit()
    session.clear()
