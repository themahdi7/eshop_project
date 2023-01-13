from django.db import models
from ckeditor.fields import RichTextField
from django.utils.text import slugify
from account_module.models import User


class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', on_delete=models.CASCADE, null=True, blank=True,
                               verbose_name='دسته بندی والد')
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='عنوان در لینک')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی مقاله ها'


class Article(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False, verbose_name='نویسنده')
    title = models.CharField(max_length=300, unique=True, verbose_name='عنوان مقاله')
    slug = models.SlugField(db_index=True, editable=False, allow_unicode=True, verbose_name='عنوان در لینک')
    image = models.ImageField(upload_to='images/article', verbose_name='تصویر مقاله')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = RichTextField(verbose_name='متن مقاله')
    selected_categories = models.ManyToManyField(ArticleCategory, verbose_name='دسته بندی ها')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انتشار')
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)


class ArticleComment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    parent = models.ForeignKey('ArticleComment', null=True, blank=True, on_delete=models.CASCADE, verbose_name='والد')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    text = models.TextField(verbose_name='متن نظر')
    # todoo check from admin and if that was true comment show on site, else comment delete

    def __str__(self):
        return f'{self.article} - {self.user} : ...{self.text[:10]}'

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله'

