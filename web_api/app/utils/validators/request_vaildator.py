from flask import Request
from werkzeug.exceptions import BadRequest


class RequestValidator:
    def __init__(
        self,
        request_type: str = "json",
        required_fields: list = [],
        field_types: dict = {},
        field_max_lengths: dict = {},
        field_validators: dict = {},
    ):
        self.__request_type = request_type
        self.__required_fields = required_fields
        self.__field_types = field_types
        self.__field_max_lengths = field_max_lengths
        self.__field_validators = field_validators
        self.__error_datails = []

    def __check_request_not_empty(self, request: Request):
        content = request.get_json() if request.is_json else request.form.to_dict()
        if not content:
            self.__error_datails.append("Request body must not be empty")

    def __check_request_type(self, request: Request):
        if self.__request_type == "json":
            if not request.is_json:
                self.__error_datails.append("Invalid Content-Type, Content-Type must be application/json")
        elif self.__request_type == "form":
            if not request.form:
                self.__error_datails.append("Invalid Content-Type, Content-Type must be multipart/form-data")
        else:
            self.__error_datails.append("Invalid request type, request type must be json or form")

    def __check_required_fields(self, request_data: dict):
        missing_fields = [
            field for field in self.__required_fields if field not in request_data
        ]
        if missing_fields:
            self.__error_datails.append(f"Missing required fields: {', '.join(missing_fields)}")

    def __check_field_types(self, request_data: dict):
        for field, field_type in self.__field_types.items():
            request_data_value = request_data.get(field, None)
            if request_data_value is not None and not isinstance(
                request_data_value, field_type
            ):
                self.__error_datails.append(f"Invalid types: {field}, expected type: `{field_type.__name__}`")

    def __check_field_max_lengths(self, request_data: dict):
        max_length_errors = [
            field
            for field in self.__field_max_lengths
            if len(str(request_data.get(field, ""))) > self.__field_max_lengths[field]
        ]
        if max_length_errors:
            self.__error_datails.append(f"Fields with too long values: {', '.join(max_length_errors)}")

    def __check_field_validators(self, request_data: dict):
        for field, validator in self.__field_validators.items():
            for request_field, request_value in request_data.items():
                if field == request_field and validator.check(str(request_value)) is False:
                    self.__error_datails.append(f"Invalid field: {field}, field does not pass validation")

    def check(self, request: Request):
        reauest_data = (
            request.get_json()
            if self.__request_type == "json" and request.is_json
            else request.form.to_dict()
        )
        self.__check_request_not_empty(request)
        self.__check_request_type(request)
        self.__check_required_fields(reauest_data)
        self.__check_field_types(reauest_data)
        self.__check_field_max_lengths(reauest_data)
        self.__check_field_validators(reauest_data)

        if len(self.__error_datails) > 0:
            raise BadRequest(self.__error_datails)
        
    def process(self, request: Request) -> dict:
        self.check(request)
        return request.get_json() if request.is_json else request.form.to_dict()