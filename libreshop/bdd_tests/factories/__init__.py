from django.contrib.auth.models import User
import factory


class AdminFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'admin@admin.com'
    username = 'admin'
    password = factory.PostGenerationMethodCall('set_password', 'admin')

    is_superuser = True
    is_staff = True
    is_active = True


class StaffMemberFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'staff@staff.com'
    username = 'staff'
    password = factory.PostGenerationMethodCall('set_password', 'staff')

    is_superuser = False
    is_staff = False
    is_active = True


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    email = 'user@user.com'
    username = 'user'
    password = factory.PostGenerationMethodCall('set_password', 'user')

    is_superuser = False
    is_staff = False
    is_active = True
