from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.


class CustomUser(AbstractUser, PermissionsMixin):
    username = models.CharField(max_length=30, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    def __str__(self):
        return self.username

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',
        blank=True,
    )


class Dashboard(models.Model):
    title = models.CharField(max_length=30)




