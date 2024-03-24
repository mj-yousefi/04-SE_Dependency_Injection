from c_db_user_repository import UserRepository
from user import User
from conifg import CUSTOMER_MIN_ORDER_COUNT, LUX_MIN_PURCHASE_AMOUNT


class UserSegmentation:

    def __init__(self, user_repo: UserRepository) -> None:
        self.user_repo = user_repo

    def segment_users(self) -> dict[str, list[User]]:
        users = self.user_repo.get_users()

        segments = {}

        segments['customer'] = [
            user for user in users if user.order_count > CUSTOMER_MIN_ORDER_COUNT
        ]
        segments['lux'] = [
            user
            for user in users
            if user.total_payment_amount > LUX_MIN_PURCHASE_AMOUNT
        ]

        return segments
