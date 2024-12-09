from django.test import TestCase
from .models import User, Role, Reservation, Time, Status, Place
import hashlib
import datetime


class TestCases(TestCase):

    def create_reservation():
        """
        Tests creation of a reservation
        """

        rs = Reservation()
        rs.user = User.objects.first()
        rs.time = Time.objects.first()
        rs.status = Status.objects.first()
        rs.type = Place.objects.first()
        rs.date = datetime.date.today()
        rs.save()

    def login(self, login, password):
        hasher = hashlib.sha256(usedforsecurity=True)
        hasher.update(str(password).encode())
        h_password = hasher.hexdigest()

        if login is None:
            return None

        if len(password) < 5:
            return None

        if (
            User.objects.filter(login=login)
            .filter(password=h_password)
            .filter(is_blocked=False)
            .exists()
        ):
            return (
                User.objects.filter(login=login)
                .filter(password=h_password)
                .filter(is_blocked=False)
                .get()
            )
        else:
            return None

    def setUp(self):

        if Role.objects.filter(name="Head").exists() is False:
            role1 = Role()
            role1.name = "Head"
            role1.save()

        if User.objects.filter(login="user").exists() == False:
            if Role.objects.filter(name="User").exists() is False:
                role1 = Role()
                role1.name = "User"
                role1.save()

            admin = User()
            admin.name = "user"
            admin.lastname = "user"
            admin.email = "user@email.com"
            admin.login = "user"
            hasher = hashlib.sha256(usedforsecurity=True)
            hasher.update(str("user123").encode())
            h_password = hasher.hexdigest()
            admin.password = h_password
            admin.role = role1
            admin.is_blocked = False
            admin.save()

        if User.objects.filter(login="admin").exists() == False:
            if Role.objects.filter(name="Admin").exists() is False:
                role = Role()
                role.name = "Admin"
                role.save()

            admin = User()
            admin.name = "admin"
            admin.lastname = "admin"
            admin.email = "admin@email.com"
            admin.login = "admin"
            hasher = hashlib.sha256(usedforsecurity=True)
            hasher.update(str("admin").encode())
            h_password = hasher.hexdigest()
            admin.password = h_password
            role = role
            admin.role = role
            admin.is_blocked = False
            admin.save()

    def test_login_success(self):
        login = "admin"
        password = "admin"
        user_assertion = User.objects.filter(login="admin").first()
        user = self.login(login, password)
        print("test 1 success")
        self.assertEqual(user_assertion, user, "Users are equal!")

    def test_login_failed(self):
        login = "admin123"
        password = "admin123"
        user_assertion = User.objects.filter(login="admin").first()
        user = self.login(login, password)
        print("test 2 success")
        self.assertNotEqual(user_assertion, user, "Users are not equal!")

    def test_login_as_user(self):
        login = "user"
        password = "user123"
        _role = User.objects.filter(login="user").first().role
        user = self.login(login, password)
        print("test 3 success")
        self.assertEqual(_role, user.role, "User with role 'User'!")

    def test_login_isnot_admin(self):
        login = "user"
        password = "user123"
        _role = User.objects.filter(login="admin").first().role
        user = self.login(login, password)
        print("test 4 success")
        self.assertNotEqual(_role, user.role, "User are not role 'Admin'!")

    def test_user_isnot_head(self):
        login = "user"
        password = "user123"
        _role = Role.objects.filter(name="Head").first()
        user = self.login(login, password)
        print("test 5 success")
        self.assertNotEqual(_role, user.role, "User are not role 'Head'!")

    def test_password_lessThanFive_failed(self):
        login = "user"
        password = "u"
        print("test 6 success")
        user = self.login(login, password)
        self.assertIsNone(user)

    def test_login_isEmpty_failed(self):
        login = None
        password = "asdasdsa"
        print("test 7 success")
        user = self.login(login, password)
        self.assertIsNone(user)
