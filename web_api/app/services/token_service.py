import jwt
import re
from datetime import datetime, timedelta
from werkzeug.exceptions import Unauthorized
from flask import request
from app.configs.config import JWT_SECRET_KEY, JWT_ACCESS_TOKEN_EXPIRE_HOURS


class JWTService:
    def __init__(self, algorithm='HS256'):
        self.secret = JWT_SECRET_KEY
        self.algorithm = algorithm
        self.exp_time = JWT_ACCESS_TOKEN_EXPIRE_HOURS * 60

    def set_exp_time(self, exp_time):
        self.exp_time = exp_time

    def generate(self, payload):
        if not isinstance(payload, dict):
            raise ValueError("Payload must be a dictionary")

        exp = datetime.utcnow() + timedelta(minutes=self.exp_time)
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
        
    def get_payload(self) -> dict:
        '''Get payload from JWT token in request header
        '''
        jwt_token_with_bearer = request.headers.get('Authorization')
        if not jwt_token_with_bearer:
            return {}

        jwt_token = re.sub(r'^Bearer ', '', jwt_token_with_bearer)
        payload = self.decode(jwt_token)
        return payload