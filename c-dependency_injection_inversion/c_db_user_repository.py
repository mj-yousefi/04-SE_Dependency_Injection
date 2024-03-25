from csv import DictReader
import csv
from user import User
import random
from abc import ABC, abstractmethod


class UserRepository(ABC):


    def __init__(self, source: str = 'all') -> None:
        """init function.

        This function receives parameter `source` which
        can be set to 'all' or 'purchase' or 'lux'.
        """
        print('********UserRepository********')
        if source == 'all':
            self.users = self._fetch_all_users()
        elif source == 'purchase':
            self.users = self._fetch_customers()
        elif source == 'lux':
            self.users = self._fetch_lux_users()
        else:
            return Exception('invalid souce')

    @abstractmethod
    def get_users(self) -> list[User]:
        pass

    @abstractmethod
    def _fetch_all_users(self):
        pass

    @abstractmethod
    def _fetch_customers(self):
        pass

    @abstractmethod
    def _fetch_lux_users(self):
        pass


class DbUserRepository(UserRepository):

    def __init__(self, source: str = 'all') -> None:
        super(DbUserRepository, self).__init__(source=source)

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


class FileUserRepository(UserRepository):

    def __init__(self, source: str = 'all') -> None:
        super(FileUserRepository, self).__init__(source=source)

    def get_users(self) -> list[User]:
        return self.users

    def __read_user_from_csv(self, file_name: str):
        users = []
        with open(
            file=file_name
        ) as read_obj:  # pass the file object to DictReader() to get the DictReader object
            csv_reader = csv.reader(read_obj, delimiter=",")
            # skip header
            next(csv_reader)
            for row in csv_reader:
                users.append(User(row[0], row[1], int(row[2]), int(row[3])))
        return users

    def _fetch_all_users(self):
        return self.__read_user_from_csv('files/data_all_users.csv')

    def _fetch_customers(self):
        return self.__read_user_from_csv('files/data_customer.csv')

    def _fetch_lux_users(self):
        return self.__read_user_from_csv('files/data_lux.csv')
