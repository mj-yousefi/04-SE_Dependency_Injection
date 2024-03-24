from b_user_segmentation import UserSegmentation
from b_db_user_repository import DbUserRepository
import unittest
from conifg import CUSTOMER_MIN_ORDER_COUNT, LUX_MIN_PURCHASE_AMOUNT


class UserSegmentation_TestCase(unittest.TestCase):

    def test_segment_lux_users(self):
        user_repo = DbUserRepository(source='lux')
        user_segmentation = UserSegmentation(user_repo=user_repo)
        segments = user_segmentation.segment_users()
        lux_segment = segments['lux']
        [
            self.assertTrue(lux_user.total_payment_amount > LUX_MIN_PURCHASE_AMOUNT)
            for lux_user in lux_segment
        ]

    def test_segment_customers(self):
        user_repo = DbUserRepository(source='purchase')
        user_segmentation = UserSegmentation(user_repo=user_repo)
        segments = user_segmentation.segment_users()
        customer_segment = segments['customer']
        [
            self.assertTrue(customer.order_count > CUSTOMER_MIN_ORDER_COUNT)
            for customer in customer_segment
        ]


if __name__ == '__main__':
    unittest.main()
