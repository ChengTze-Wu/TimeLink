from flask import Request, session, redirect, url_for, current_app
from web_api.db.models import User
from functools import wraps
import re
import jwt

class RequestValidator:
    '''
    Validates a request to check if it meets the criteria:
    - Content-Type is application/json or application/x-www-form-urlencoded
    - Required fields are present
    - Field types are correct
    - Field lengths are correct

    Parameters:
    request (Request): The request to validate

    Returns:
    RequestValidator: The RequestValidator instance

    Example:
    >>> request_validator = RequestValidator(request)
    '''
    def __init__(self, request: Request):
        self.__request = request
        self.__request_type = 'json'
        self.__required_fields = []
        self.__field_types = {}
        self.__field_max_lengths = {}
        self.__field_validators = {}
        self.__message = {}
        self.__data = self.__request.get_json() if self.__request.is_json else self.__request.form.to_dict()

    def config(self, request_type: str='json', required_fields: list=None, field_types: dict=None, field_max_lengths: dict=None, field_validators: dict=None):
        '''
        Configures the validator

        Parameters:
        request_type (str): The request type, either 'json' or 'form'
        required_fields (list): A list of required fields
        field_types (dict): A dictionary of field types
        field_max_lengths (dict): A dictionary of field maximum lengths
        field_validators (dict): A dictionary of field validators

        Returns:
        None

        Example:
        >>> request_validator.config(
            request_type='json',
            required_fields=['email', 'username', 'password', 'name'],
            field_types={
                'email': str,
                'username': str,
                'password': str,
                'name': str,
            },
            field_max_lengths={
                'email': 255,
                'username': 255,
                'password': 255,
                'name': 255,
            },
            field_validators={
                'email': EmailValidator,
                'password': PasswordValidator,
            }
        )
        '''
        if request_type is not None:
            self.__request_type = request_type
        if required_fields is not None:
            self.__required_fields = required_fields
        if field_types is not None:
            self.__field_types = field_types
        if field_max_lengths is not None:
            self.__field_max_lengths = field_max_lengths
        if field_validators is not None:
            self.__field_validators = field_validators

    def check(self):
        return (
            self.__check_request_not_empty() and
            self.__check_request_type() and
            self.__check_required_fields() and
            self.__check_field_types() and
            self.__check_field_max_lengths() and
            self.__check_field_validators()
        )
    
    def __check_request_not_empty(self):
        if not self.__data:
            self.__message = "Request body must not be empty"
            return False
        return True

    def __check_request_type(self):
        if self.__request_type == 'json':
            if not self.__request.is_json:
                self.__message = "Content-Type must be application/json"
                return False
        elif self.__request_type == 'form':
            if not self.__request.form:
                self.__message = "Content-Type must be application/x-www-form-urlencoded"
                return False
        return True

    def __check_required_fields(self):
        missing_fields = [field for field in self.__required_fields if field not in self.__data or not self.__data[field]]
        if missing_fields:
            self.__message = f"Missing required fields: {', '.join(missing_fields)}"
            return False
        return True

    def __check_field_types(self):
        is_valid = True
        field_types = []
        for field in self.__field_types:
            if self.__data.get(field) and not isinstance(self.__data.get(field), self.__field_types[field]):
                field_types.append(field)
                is_valid = False
            self.__message = f"Fields with invalid types: {', '.join(field_types)}"
        return is_valid

    def __check_field_max_lengths(self):
        length_errors = [field for field in self.__field_max_lengths if len(self.__data.get(field, '')) > self.__field_max_lengths[field]]
        if length_errors:
            self.__message = f"Fields with invalid lengths: {', '.join(length_errors)}"
            return False
        return True
    
    def __check_field_validators(self):
        is_valid = True
        field_validators = []
        for field in self.__field_validators:
            if self.__data.get(field) and not self.__field_validators[field].check(self.__data.get(field, '')):
                field_validators.append(field)
                is_valid = False
            self.__message = f"Fields with invalid values: {', '.join(field_validators)}"
        return is_valid
    
    @property
    def message(self):
        return self.__message


class EmailValidator:
    @staticmethod
    def check(email: str) -> bool:
        '''
        Validates an email address to check if it meets the criteria:
        - Contains an @ symbol
        - Contains a period after the @ symbol

        Parameters:
        email (str): The email address to validate

        Returns:
        bool: True if the email address is valid, False otherwise
        '''
        return bool(re.search(r'[^@]+@[^@]+\.[^@]+', email))


class PasswordValidator:
    @staticmethod
    def check(password: str) -> bool:
        '''
        Validates a password to check if it meets the criteria:
        - At least 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one digit
        - At least one special character: `@$!%*?&.`

        Parameters:
        password (str): The password to validate

        Returns:
        bool: True if the password is valid, False otherwise

        Example:
        >>> PasswordValidator.check('Abc123!@#')
        True
        '''
        return bool(re.search(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8}', password))
    

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if session.get('usertoken'):
            try:
                usertoken = jwt.decode(session.get('usertoken'), current_app.config['SECRET_KEY'], algorithms=["HS256"])
            except jwt.exceptions.ExpiredSignatureError or jwt.exceptions.InvalidSignatureError:
                session.pop('usertoken', None)
                return redirect(url_for('home.index'))
            username = usertoken["username"]
        else:
            username = ""
        dbData = User.query.filter_by(username=username).first()
        if not dbData:
            return redirect(url_for('home.index'))
        return func(*args, **kwargs)
    return decorated