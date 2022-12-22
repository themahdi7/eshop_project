from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {
        'slug': ['title'],
    }
    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_filter = ['category', 'price', 'is_active']



admin.site.register(models.Product, ProductAdmin)
# admin.site.register(models.Product)
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTags)
