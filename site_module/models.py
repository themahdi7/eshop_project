from turtle import position

from django.db import models


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=200, verbose_name='نام سایت')
    site_url = models.CharField(max_length=200, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name='آدرس')
    phone = models.CharField(max_length=200, null=True, blank=True, verbose_name='تلفن')
    fax = models.CharField(max_length=200, null=True, blank=True, verbose_name='فکس')
    email = models.CharField(max_length=200, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت')
    about_us_text = models.TextField(verbose_name='متن درباره ما')
    site_logo = models.ImageField(upload_to='images/site-settings', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name


class Slider(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(verbose_name='لینک')
    url_title = models.CharField(max_length=200, verbose_name='عنوان لینک')
    description = models.TextField(verbose_name='توضیحات اسلایدر')
    image = models.ImageField(upload_to='images/slider', verbose_name='تصویر اسلایدر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    # time field for show on site

    class Meta:
        verbose_name = 'اسلایدر'
        verbose_name_plural = 'اسلایدر ها'

    def __str__(self):
        return self.title


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی لینک های فوتر'

    def __str__(self):
        if self.is_active:
            return f'{self.title} - فعال'
        return f'{self.title} - غیرفعال '


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(verbose_name='لینک')
    footer_link_box = models.ForeignKey(to=FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'

    def __str__(self):
        return f'{self.title} - {self.footer_link_box.title}'


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات',
        product_detail = 'product_detail', 'صفحه جزییات محصولات',


    title = models.CharField(max_length=200, verbose_name='عنوان بنر')
    url = models.URLField(null=True, blank=True, verbose_name='لینک')
    image = models.ImageField(upload_to='images/banner', verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='جایگاه نمایشی')

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'

    def __str__(self):
        return self.title


