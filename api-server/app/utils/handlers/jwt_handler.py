import os
import jwt
import re
from datetime import datetime, timedelta
from werkzeug.exceptions import Unauthorized

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
JWT_ACCESS_TOKEN_EXPIRE_HOURS = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRE_HOURS", 24))
if JWT_SECRET_KEY is None:
    raise ValueError("JWT_SECRET_KEY Environment Variable is not set")


class JWTHandler:
    def __init__(self, algorithm="HS256"):
        self.secret = JWT_SECRET_KEY
        self.algorithm = algorithm
        self.exp_second = JWT_ACCESS_TOKEN_EXPIRE_HOURS * 60 * 60

    def set_exp_time(self, exp_time):
        self.exp_second = exp_time

    def generate(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")

        exp = datetime.utcnow() + timedelta(seconds=self.exp_second)
        payload.update({"exp": exp, "iat": datetime.utcnow()})

        token = jwt.encode(payload, self.secret, algorithm=self.algorithm)
        return token

    def decode(self, token):
        try:
            return jwt.decode(token, self.secret, algorithms=[self.algorithm])
        except jwt.ExpiredSignatureError:
            raise Unauthorized("Token is expired")
        except jwt.InvalidTokenError:
            raise Unauthorized("Token is invalid")

    def get_payload(self, authorization_header) -> dict:
        if not authorization_header:
            return {}
        jwt_token = re.sub(r"^Bearer ", "", authorization_header)
        payload = self.decode(jwt_token)
        return payload
    
    def get_payload_from_flask(self) -> dict:
        '''Get payload from flask request object'''
        from flask import request
        jwt_token_with_bearer = request.headers.get("Authorization")
        if not jwt_token_with_bearer:
            return {}

        jwt_token = re.sub(r"^Bearer ", "", jwt_token_with_bearer)
        payload = self.decode(jwt_token)
        return payload