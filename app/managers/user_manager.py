"""User Manager"""
from typing import Final, Union
from datetime import datetime
from logging import Logger
from app.models.user_entity import UserEntity

# Max number of unsuccessful logins in a row
_LOGIN_COUNT_LIMIT: Final[int] = 10
# Timer in seconds to reset LOGIN_COUNT_LIMIT to 0
_LOGIN_COUNT_RESET: Final[int] = 600

def is_user_below_max_login_count(user) -> bool:
    """Returns if user is below limit."""
    return user.login_count < _LOGIN_COUNT_LIMIT

def tick_user_login_count(user: UserEntity) -> None:
    """Increments or resets user.login_count based on _LOGIN_COUNT_RESET.
    Requires manual database commit."""
    current_date = datetime.utcnow()

    if (current_date - user.last_try).total_seconds() > _LOGIN_COUNT_RESET:
        user.login_count = 0

    else:
        user.login_count = user.login_count + 1

def load_user(user_identifier: str, logger: Logger) -> Union[UserEntity, None]:
    """Returns the user from successful session_auth else None"""
    try:
        user_id, pwd_check = user_identifier.split(UserEntity.LOGIN_ID_SEPARATOR, 1)

        user = UserEntity.query.filter_by(id=int(user_id)).first()

        if user and user.session_auth(pwd_check):
            return user
    except ValueError as ex:
        logger.warning('login_manager: %s', ex)
    return None
