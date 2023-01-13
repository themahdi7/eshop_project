from django.db import models
from django.urls import reverse
from django.utils.text import slugify

from account_module.models import User


class ProductTags(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")

    class Meta:
        verbose_name = 'برچسب'
        verbose_name_plural = 'برچسب های محصولات'

    def __str__(self):
        return f"{self.caption}"


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name="نام برند", db_index=True)
    url_title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان در url")
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'برند'
        verbose_name_plural = 'برند های محصولات'

    def __str__(self):
        return f"{self.title}"


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    url_title = models.CharField(max_length=300, verbose_name="url عنوان در")
    parent = models.ForeignKey('ProductCategory', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return f"({self.title} - {self.url_title})"


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name='product_categories',
                                      verbose_name="دسته بندی محصول")
    tag = models.ManyToManyField(ProductTags, verbose_name="برچسب های محصول")
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name="برند", null=True, blank=True)
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name='تصویر محصول')
    price = models.IntegerField(default=0, verbose_name='قیمت')
    short_description = models.CharField(max_length=360, null=True, db_index=True, verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name="توضیحات اصلی")
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(default=False, verbose_name='حذف شده / حذف نشده')
    slug = models.SlugField(db_index=True, editable=False, allow_unicode=True, verbose_name='عنوان در لینک')
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('product:product_detail', args=[self.slug])

    def __str__(self):
        return f"{self.title}"


class ProductVisit(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    ip = models.CharField(max_length=30, verbose_name='آی پی کاربر')
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, verbose_name='کاربر')

    class Meta:
        verbose_name = 'بازدید محصول'
        verbose_name_plural = 'بازدید های محصول'

    def __str__(self):
        return f"({self.product} - {self.ip})"


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product-gallery', verbose_name='تصویر')

    class Meta:
        verbose_name = 'گالری محصول'
        verbose_name_plural = 'گالری محصولات'

    def __str__(self):
        return self.product.title
