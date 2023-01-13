# Generated by Django 4.1.4 on 2023-01-11 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_sitebanner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitebanner',
            name='position',
            field=models.CharField(choices=[('product_list', 'صفحه لیست محصولات'), ('product_detail', 'صفحه جزییات محصولات'), ('about_us', 'درباره ما')], max_length=200, verbose_name='جایگاه نمایشی'),
        ),
    ]