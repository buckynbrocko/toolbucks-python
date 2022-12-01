import pytest

from datatypes.email import QUICK_EMAIL_REGEX


class Test_QuickEmailRegEx:
    @pytest.mark.parametrize("email", [
        "abc@def.com",
        "abc@def.co",
    ])
    def test_true(self, email: str):
        assert QUICK_EMAIL_REGEX.match(email) is not None

    @pytest.mark.parametrize("email", [
        "abc@@def.com",
        "abc@@defcom",
    ])
    def test_false(self, email: str):
        assert QUICK_EMAIL_REGEX.match(email) is None
