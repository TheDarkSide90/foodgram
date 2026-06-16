import string
import random

from .constants import GENERATE_RANGE, CODE_LENGTH
from .models import ShortLink

CHARS = string.ascii_letters + string.digits


def generate_short_code(length=CODE_LENGTH):
    for _ in range(GENERATE_RANGE):
        code = ''.join(random.choice(CHARS) for _ in range(length))
        if not ShortLink.objects.filter(code=code).exists():
            return code
    raise RuntimeError("Не удалось сгенерировать уникальный код")
