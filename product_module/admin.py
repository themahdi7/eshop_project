from django.contrib import admin
from .models import Product


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'],
        'title': ['slug']
    }
    list_display = ['title', 'price', 'rating', 'is_active']



admin.site.register(Product, ProductAdmin)
