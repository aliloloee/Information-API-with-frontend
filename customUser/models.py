from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.core.exceptions import ValidationError

from persian_tools import national_id


def validate_national_id(value) :
    if not national_id.validate(value) :
        raise ValidationError('Wrong national id !!')



class MyUserManager(BaseUserManager):
    def create_user(self, username, password=None):
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            username = username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
                        username,
                        password
                    )

        user.is_active = True
        user.is_staff = True
        user.is_admin = True
        user.is_superuser = True

        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=100, unique=True, validators=[validate_national_id])
    fullname = models.CharField(max_length=150, blank=True, null=True)

    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USER_TYPE_CHOICES = (
        (1, 'doctor'),
        (2, 'nurse'),
        (3, 'patient'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES, blank=True, null=True)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def get_fullName(self) :
        return f'{self.fullname}'

    def __str__(self) :
        if self.fullname != None :
            return self.fullname
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class DefinedPeople(models.Model) :
    TYPE_CHOICES = (
        (1, 'doctor'),
        (2, 'nurse'),
        (3, 'staff'),
    )
    national_id = models.CharField(max_length=20, unique=True, validators=[validate_national_id])
    user_type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)

    class Meta :
        verbose_name = 'Defined People'
        verbose_name_plural = 'Defined People'

    def __str__(self) :
        r = DefinedPeople.TYPE_CHOICES[self.user_type - 1][1]
        return f'{self.national_id} is defined as {r.upper()} in the system'