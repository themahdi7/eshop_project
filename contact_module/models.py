from django.db import models
from utils.email_service import send_email


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name="عنوان")
    full_name = models.CharField(max_length=300, verbose_name="نام و نام خانوادگی")
    email = models.EmailField(max_length=300, verbose_name="ایمیل")
    message = models.TextField(verbose_name="متن تماس با ما")
    created_date = models.DateField(verbose_name="تاریخ ایجاد", auto_now_add=True)
    response = models.TextField(verbose_name="متن پاسخ تماس با ما", null=True, blank=True)
    is_read_by_admin = models.BooleanField(verbose_name="خوانده شده توسط ادمین", default=False)
    send_email = models.BooleanField(default=False, editable=False, verbose_name="ایمیل پاسخ ارسال شده")

    class Meta:
        verbose_name = "تماس با ما"
        verbose_name_plural = "لیست تماس با ما"

    def __str__(self):
        return f"{self.title} - {self.full_name}"

    def save(self, *args, **kwargs):
        if self.is_read_by_admin and self.response and self.send_email == False:
            self.send_email = True
            test = True
            user_email = self.email
            admin_response = self.response
            send_email('پیام شما را دریافت کردیم', user_email, {'user': user_email, 'admin_response': admin_response},
                       'emails/contact_response.html')
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    image = models.ImageField(upload_to='images')
