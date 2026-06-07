import string
import random

from .models import ShortLink


def generate_short_code():
    chars = string.ascii_letters + string.digits

    while True:
        code = ''.join(random.choice(chars) for _ in range(6))
        if not ShortLink.objects.filter(code=code).exists():
            return code
