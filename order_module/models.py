from django.db import models

from account_module.models import User
from product_module.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شد / نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    def calculate_tax(self):
        tax_amount: int = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                tax_amount += (order_detail.final_price * order_detail.count) * 9 / 100
            return tax_amount
        else:
            for order_detail in self.orderdetail_set.all():
                tax_amount += (order_detail.product.price * order_detail.count) * 9 / 100
            return int(tax_amount)


    def calculate_amount(self):
        # calculate amount without tax
        total_amount: int = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price * order_detail.count
            return total_amount
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product.price * order_detail.count
            return int(total_amount)

    def calculate_total(self):
        # calculate total amount with tax
        total: int = 0
        total += self.calculate_amount() + self.calculate_tax()
        return int(total)


    def __str__(self):
        return str(self.user)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, editable=False, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'جزییات سبد های خرید'

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return f'{self.product} - {self.order}'

    def save(self, *args, **kwargs):
        self.final_price = self.product.price
        super().save(*args, **kwargs)
