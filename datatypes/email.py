import re
from re import Pattern
from typing import Callable


class ValidatedString(str):
    _ErrorClass = ValueError
    _validator_fn: Callable[[str], bool]

    def __post_init__(self): ...

    def __init__(self) -> None:
        if not self.is_valid:
            message = self.validation_error_message()
            raise self._ErrorClass(message)
        self.__post_init__()

    @property
    def is_valid(self) -> bool:
        return self.validate()

    def validate(self) -> bool:
        return True

    def validation_error_message(self) -> str:
        return f"Validation failed for class '{self.__class__.__name__}'"


# a la https://www.emailregex.com/
EMAIL_REGEX = re.compile("""(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])""")
QUICK_EMAIL_REGEX = re.compile(
    r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")


def is_email_address(
    string: str,
    regex: Pattern[str] = QUICK_EMAIL_REGEX
) -> bool:
    return regex.match(string) is not None


class EmailAddress(ValidatedString):
    local_part: str
    domain: str
    regex: Pattern[str] = QUICK_EMAIL_REGEX

    def __init__(self, value):
        parts = self.split("@")
        assert len(parts) == 2
        self.local_part, self.domain = parts

    def validate(self) -> bool:
        return is_email_address(self, regex=self.regex)

    def __str__(self) -> str:
        return self.local_part + '@' + self.domain

    def __json__(self) -> str:
        return str(self)


class StrictEmailAddress(EmailAddress):
    regex: Pattern[str] = EMAIL_REGEX
