from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
# Create your models here.
from .managers import UserManager


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length=50,unique=True)
    phonenumber = models.CharField(max_length=10,unique=True)
    is_soundhead = models.BooleanField(default = False)
    is_setuphead = models.BooleanField(default = False)
    is_superuser = models.BooleanField(default=False)
    #is_staff = models.BooleanField(default=False)
    is_teamadmin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phonenumber','is_setuphead','is_soundhead','is_teamadmin','is_active']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_superuser


