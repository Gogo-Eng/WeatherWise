#!/usr/bin/env python3
"""
Hashing and verifying passwords
"""

import bcrypt
from models.db import DB # type: ignore
from models.user import User # type: ignore
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ returns a passwd hash """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()

    hashed_password = bcrypt.hashpw(password_bytes, salt)

    return hashed_password


def _generate_uuid() -> str:
    """ returns a uuid4 str """
    unique_id = str(uuid4())
    return unique_id


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """ initiallize object """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers users """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists.")
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ validates credentials """
        try:
            user = self._db.find_user_by(email=email)
            byte_password = password.encode('utf-8')
            hashed_password = user.hashed_password.encode('utf-8')
            print(f"User found: {user.email}, Hashed password in DB: {hashed_password}")
        
            if bcrypt.checkpw(byte_password, hashed_password):
                print("Password matched")
                return True
            else:
                print("Password did not match")
                return False
        except Exception as e:
            print(f"Error during login: {e}")
            return False

    def create_session(self, email: str) -> str:
        """ creates a new session for user with email """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        session_id = _generate_uuid()
        self._db.update_user(user.id, session_id=session_id)
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ gets user by session_id """
        if not session_id:
            return None
        else:
            try:
                user = self._db.find_user_by(session_id=session_id)
                return user
            except NoResultFound:
                return None

    def destroy_session(self, user_id: int) -> None:
        """ removes user's session_id """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            return None

    def get_reset_password_token(self, email: str) -> str:
        """ updates a users reset token field """
        try:
            user = self._db.find_user_by(email=email)
            token = _generate_uuid()
            self._db.update_user(user.id, reset_token=token)
            return token
        except NoResultFound:
            raise ValueError("User DNE")

    def update_password(self, reset_token: str, password: str) -> None:
        """ updates users password """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed_password,
                             reset_token=None)
