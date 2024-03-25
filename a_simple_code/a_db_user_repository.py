from user import User
import random


class DbUserRepository:

    def __init__(self, source: str = 'all') -> None:
        """init function.

        This function receives parameter `source` which
        can be set to 'all' or 'purchase' or 'lux'.
        """
        if source == 'all':
            self.users = self._fetch_all_users()
        elif source == 'purchase':
            self.users = self._fetch_customers()
        elif source == 'lux':
            self.users = self._fetch_lux_users()
        else:
            return Exception('invalid souce')

    def get_users(self) -> list[User]:
        return self.users

    def _fetch_all_users(self):
        users = []
        for i in range(20):
            order_count = random.randint(0, 2)
            avg_amount = random.randint(100000, 20000000)
            users.append(
                User(
                    order_count=order_count,
                    total_payment_amount=order_count * avg_amount,
                )
            )
        return users

    def _fetch_customers(self):
        return [
            User(
                order_count=random.randint(1, 5),
                total_payment_amount=10000 + 20 * random.randint(0, 10),
            )
            for i in range(20)
        ]

    def _fetch_lux_users(self):
        users = []
        for i in range(20):
            order_count = random.randint(1, 5)
            avg_amount = random.randint(15000000, 20000000)
            users.append(
                User(
                    order_count=order_count,
                    total_payment_amount=order_count * avg_amount,
                )
            )
        return users
