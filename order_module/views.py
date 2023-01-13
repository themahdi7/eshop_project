from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from product_module.models import Product
from .models import Order, OrderDetail


def add_product_to_order(request):
    product_id = request.GET.get('product_id')
    count = int(request.GET.get('count'))
    if count < 1:
        return JsonResponse({
            'status': 'invalid count',
            'title': 'توجه',
            'text': 'مقدار وارد شده معتبر نمی باشد',
            'icon': 'warning',

        })

    if request.user.is_authenticated:
        product = Product.objects.filter(id=product_id, is_active=True, is_delete=False).first()
        if product is not None:
            current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
            current_order_detail = current_order.orderdetail_set.filter(product_id=product_id).first()
            if current_order_detail is not None:
                current_order_detail.count += count
                current_order_detail.save()
            else:
                new_detail = OrderDetail(order_id=current_order.id, product_id=product_id, count=count)
                new_detail.save()

            return JsonResponse({
                'status': 'success',
                'title': 'موفقیت آمیز',
                'text': 'محصول مورد نظر با موفقیت به سبد خرید اضافه شد',
                'icon': 'success',

            })
        else:
            return JsonResponse({
                'status': 'not_found',
                'title': 'خطا',
                'text': 'محصول مورد نظر یافت نشد',
                'icon': 'error',
            })


    else:
        return JsonResponse({
            'status': 'not_authorized',
            'title': 'خطا',
            'text': 'برای افزودن سبد خرید ابتدا می بایست در سایت ثبت نام کنید',
            'icon': 'error',

        })
