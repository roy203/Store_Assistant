import re

_DIGITS_RE = re.compile(r"\D")


def validate_phone(phone: str) -> bool:
    if not phone:
        return False
    digits = _DIGITS_RE.sub("", phone)
    if len(digits) == 10:
        return True
    if len(digits) == 11 and digits[0] == "1":
        return True
    return False


def normalize_phone(phone: str) -> str:
    digits = _DIGITS_RE.sub("", phone)
    if len(digits) == 11 and digits[0] == "1":
        digits = digits[1:]
    return digits
