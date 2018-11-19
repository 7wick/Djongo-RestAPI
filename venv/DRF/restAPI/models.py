from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager

class UserModelManager(BaseUserManager):

    def create_user(self, username, password, email):
        if not username:
            raise ValueError('username is required')
        if not email:
            raise ValueError('email is required')

        user = self.model(
            username = username
        )
        user.set_password(password)
        user.save()
        return user

    def create_staffuser(self, username, password, email):
        user = self.create_user(username, password,email)
        user.staff = True
        user.save()
        return user

    def create_superuser(self, username, password, email):
        user = self.create_user(username, password, email)
        user.staff = True
        user.is_superuser = True
        # user.is_active = True
        user.save()
        return user

class UserModel(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=50, unique=True, blank=False)
    password = models.CharField(max_length=20, blank=False)
    email = models.EmailField(unique=True, blank=False)
    password_confirm = models.CharField(max_length=10, blank=False)
    length = models.IntegerField(blank=True)

    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False)
    is_superuser = False

    objects = UserModelManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

class metadata(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name_length = models.IntegerField()