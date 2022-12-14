from django.db import models



class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    price = models.IntegerField(verbose_name='قیمت')



    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = ('محصول')
        verbose_name_plural = ('محصولات')