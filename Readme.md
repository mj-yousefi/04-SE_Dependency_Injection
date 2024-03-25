# SE-DependencyInjection


## Project Description

This project illustrates dependency injection and dependency inversion concepts in a simple user segmentation project.

There is a ```User``` class that contains users information such as id, order count, and the total amount that the user spends. We have a DataRepository class which returns users, and a UserSegmentaion which segments users. To test their functionality, we write a unit test class.


## Segments

lux: User whose total payment exceeds 20000000.
customer: User who has purchased at least one time.

## Entities

This is ```User``` class:

```
@dataclass
class User:
    id: str = ''.join(random.choices(string.ascii_lowercase, k=8))
    phone_number: str = '0912' + ''.join(random.choices(string.digits, k=7))
    order_count: int = 0
    total_payment_amount: int = 0
```

The ```DbUserRepository``` class fetches data from the database (in this example we generate sample data).

```
class DbUserRepository:

    def __init__(self, source: str = 'all') -> None:
        ...

    def get_users(self) -> list[User]:
       ...

    def _fetch_all_users(self):
        ...

    def _fetch_customers(self):
        ...

    def _fetch_lux_users(self):
        ...
```

And, ```UserSegemntaion``` segments User:

```

class UserSegmentation:

    def segment_users(self) -> dict[str, list[User]]:
        """
        Returns a dict of segments which key is segment and value is the list of users in that segment
        """
        ...
```

## Step 1- Implement a simple user segmentation

In step 1, we are going to implement user segmentation. I put all the step 1 code into a_simple_code directory. Let's implement the ```segment_users``` method. This method creates a reference of DbUserRepository and getUsers. Then, this segment user:

```
    def segment_users(self) -> dict[str, list[User]]:
        user_repo =  DbUserRepository(source='all')
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

```

### So, what is the problem here? 


The problem is that UserSegmentation depends on DbUserRepository and creates an instance of DbUserRepository. This makes it hard to change the behavior of this dependency. In other words, every time, we want to change the behavior of UserRepository, we have to change this inside the UserSegmentation class. For example, if we want to segment only customers, we need to change ```segment_users()``` method like this:


```
    def segment_users(self) -> dict[str, list[User]]:
        # we hae to change the source parameter
        user_repo =  DbUserRepository(source='purchase')
        users = user_repo.get_users()
        ...
        
```

This can make it hard to develop or reuse ```UserSegmentation``` class. As we can see in UserSegmentation_TestCase, we cannot directly test customer users (there is no way to change the source parameter outside ```UserSegmentation``` class except using mock, which is hard to implement!). Therefore, it is recommended that we inject dependency (here DbUserRepository) from outside of the class, which we will do in the next step.


## step 2- Using Dependency Injection

To make ```UserSegmentation``` more extensible, we inject ```DbUserRepository``` into it. I put all the scripts that belong to this step into the b-dependency_injection directory. We take ```DbUserRepository``` as an initializer in the ```__init__``` function (or constructor). Now the ```UserSegmentation``` class become like this:

```
class UserSegmentation:

    def __init__(self, user_repo: DbUserRepository) -> None:
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

```

This, enables us to set  ```DbUserRepository``` as we want to be. For instance, in the ```UserSegmentation_TestCase```, now we can write separate test cases for luxury users and customers:


```
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

```

We solve the dependency problem in this step. We separated the responsibility of creating an instance of dependency class (```DbUserRepository```) and using it. Now, ```UserSegmentation``` only uses it! However, what if we want to replace DbUserReposiory with another class? Suppose we want to use a stream or file repository, again, we have to change ```UserSegmentaion``` class!!. In the next step, we are going to solve this problem by dependency inversion. 

## Step 3- Dependency Inversion

In this step, we add another layer between dependencies, to make it easier to develop our project. 

We want to create an abstract class of the repository and pass it to ```UserSegmentation``` class. Then, the ```UserSegmentation``` class does not have to know about the exact type of repository. Like in previous steps, I put all scripts in one directory which is c-dependency_injection_inversion.

So, let's create an abstract class called ```UserRepository```:

```
class UserRepository(ABC):

    # source can be ''

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

```

Now, We should implement ```UserRepository```. First, we create ```DbUserRepository```:

```
class DbUserRepository(UserRepository):

    # source can be ''
    def __init__(self, source: str = 'all') -> None:
        super(DbUserRepository, self).__init__(source=source)

    def get_users(self) -> list[User]:
        return self.users

    def _fetch_all_users(self):
        ...

    def _fetch_customers(self):
        ...

    def _fetch_lux_users(self):
        ...
```

And, ```FileUserRepository```:


class FileUserRepository(UserRepository):

    def __init__(self, source: str = 'all') -> None:
        super(FileUserRepository, self).__init__(source=source)

    def get_users(self) -> list[User]:
        return self.users

    def __read_user_from_csv(self, file_name: str):
        ...

    def _fetch_all_users(self):
        return self.__read_user_from_csv('files/data_all_users.csv')

    def _fetch_customers(self):
        return self.__read_user_from_csv('files/data_customer.csv')

    def _fetch_lux_users(self):
        return self.__read_user_from_csv('files/data_lux.csv')


Finally, we change the ```UserSegmentation``` class in a way that takes ```UserRepository```. Now, this only know about ```get_users()``` method:

```
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
```

Dependency inversion is done! We can easily write test cases for each UserReposiory. We only need to instantiate different types of ```UserRepository``` and pass them to ```UserSegmentation``` class. For example, to test segment customers from File and Database we can write :

```
    def test_segment_customers_db(self):
        user_repo = DbUserRepository(source='purchase')
        user_segmentation = UserSegmentation(user_repo=user_repo)
        segments = user_segmentation.segment_users()
        customer_segment = segments['customer']
        [
            self.assertTrue(customer.order_count > CUSTOMER_MIN_ORDER_COUNT)
            for customer in customer_segment
        ]

    def test_segment_customers_file(self):
        user_repo = FileUserRepository(source='purchase')
        user_segmentation = UserSegmentation(user_repo=user_repo)
        segments = user_segmentation.segment_users()
        customer_segment = segments['customer']
        [
            self.assertTrue(customer.order_count > CUSTOMER_MIN_ORDER_COUNT)
            for customer in customer_segment
        ]
```
