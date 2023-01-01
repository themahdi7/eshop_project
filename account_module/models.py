from django.db import models
from django.contrib.auth.models import AbstractUser


# Customize User model
class User(AbstractUser):
    avatar = models.ImageField(verbose_name='تصویر پروفایل', null=True, blank=True)
    email_active_code = models.CharField(max_length=100, verbose_name='کد فعالسازی ایمیل', editable=False)

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        return self.get_username()
