from django.contrib import admin
from . import models


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'brand', 'is_active', 'is_delete']
    list_filter = ['category', 'price', 'brand', 'title', 'is_active']


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'url_title', 'parent']
    list_filter = ['title', 'is_active', 'url_title', 'parent']


class ProductVisitAdmin(admin.ModelAdmin):
    list_display = ['product', 'user', 'ip']
    list_filter = ['product', 'user', 'ip']


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product']
    list_filter = ['product']

admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.ProductCategory, ProductCategoryAdmin)
admin.site.register(models.ProductTags)
admin.site.register(models.ProductBrand)
admin.site.register(models.ProductGallery, ProductGalleryAdmin)
admin.site.register(models.ProductVisit, ProductVisitAdmin)

