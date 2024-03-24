from a_db_user_repository import DbUserRepository
from user import User
from conifg import CUSTOMER_MIN_ORDER_COUNT, LUX_MIN_PURCHASE_AMOUNT


class UserSegmentation:

    def segment_users(self) -> dict[str, list[User]]:
        user_repo = DbUserRepository()
        users = user_repo.get_users()

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
