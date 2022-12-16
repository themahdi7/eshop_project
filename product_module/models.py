from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse

class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], default=0, verbose_name='امتیاز')
    short_description = models.CharField(max_length=360,null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=False, verbose_name='وضعیت انتشار')

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = ('محصول')
        verbose_name_plural = ('محصولات')

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.id])

