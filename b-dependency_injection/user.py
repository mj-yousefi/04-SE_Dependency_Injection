from dataclasses import dataclass
import random
import string


@dataclass
class User:
    id: str = ''.join(random.choices(string.ascii_lowercase, k=8))
    phone_number: str = '0912' + ''.join(random.choices(string.digits, k=7))
    order_count: int = 0
    total_payment_amount: int = 0
