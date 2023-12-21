import re
from abc import ABC, abstractmethod


class FieldValidator(ABC):
    @abstractmethod
    def check(self, value: str) -> bool:
        pass


class PasswordValidator(FieldValidator):
    @staticmethod
    def check(password: str) -> bool:
        """
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
        """

        return bool(
            re.search(
                r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8}",
                password,
            )
        )


class EmailValidator(FieldValidator):
    @staticmethod
    def check(email: str) -> bool:
        """
        Validates an email address to check if it meets the criteria:
        - Contains an @ symbol
        - Contains a period after the @ symbol

        Parameters:
        email (str): The email address to validate

        Returns:
        bool: True if the email address is valid, False otherwise
        """

        return bool(re.search(r"[^@]+@[^@]+\.[^@]+", email))
