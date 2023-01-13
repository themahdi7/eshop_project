from django.contrib import admin
from . import models


class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid', 'payment_date']
    list_filter = ['user', 'is_paid', 'payment_date']


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'final_price', 'count']
    list_filter = ['product', 'final_price', 'count']


admin.site.register(models.Order, OrderAdmin)
admin.site.register(models.OrderDetail, OrderDetailAdmin)
