# Generated by Django 4.1.4 on 2022-12-28 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0006_product_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='Created',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='product',
            name='Updated',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
