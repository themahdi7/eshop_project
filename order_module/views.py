import json
from datetime import time
import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from product_module.models import Product
from .models import Order, OrderDetail


# Zarin Pall informations
MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
amount = 11000  # Rial / Required
description = "نهایی کردن خرید"  # Required
email = 'email@example.com'  # Optional
mobile = '09123456789'  # Optional
# Important: need to edit for realy server.
CallbackURL = 'http://127.0.0.1:7000:7000/order/verify-payment/'


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


@login_required
def request_payment(request):
    current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
    total_price = current_order.calculate_total()
    if total_price == 0:
        return redirect(reverse('panel:user_order_page'))

    req_data = {
        "merchant_id": MERCHANT,
        "amount": total_price * 10,
        "callback_url": CallbackURL,
        "description": description,
    }
    req_header = {"accept": "application/json",
                  "content-type": "application/json'"}
    req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
        req_data), headers=req_header)
    authority = req.json()['data']['authority']
    if len(req.json()['errors']) == 0:
        return redirect(ZP_API_STARTPAY.format(authority=authority))
    else:
        e_code = req.json()['errors']['code']
        e_message = req.json()['errors']['message']
        return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")


@login_required
def verify_payment(request):
    print(request.user)
    print(request.user.id)
    t_authority = request.GET['Authority']
    if request.GET.get('Status') == 'OK':
        current_order, created = Order.objects.get_or_create(is_paid=False, user_id=request.user.id)
        total_price = current_order.calculate_total()
        req_header = {"accept": "application/json",
                      "content-type": "application/json'"}
        req_data = {
            "merchant_id": MERCHANT,
            "amount": total_price * 10,
            "authority": t_authority
        }
        req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
        if len(req.json()['errors']) == 0:
            t_status = req.json()['data']['code']
            if t_status == 100:
                current_order.is_paid = True
                current_order.payment_date = time()
                current_order.save()

                ref_str = str(req.json()['data']['ref_id'])
                return render(request, 'order_module/payment_result.html',
                              {'success': f'تراکنش شما با کد پیگیری{ref_str} با موفقیت انجام شد'})
            elif t_status == 101:
                return render(request, 'order_module/payment_result.html',
                              {'info': 'این تراکنش قبلا پرداخت شده است'})
            else:
                return render(request, 'order_module/payment_result.html',
                              {'error': str(req.json()['data']['ref_id'])})
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            # return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
            return render(request, 'order_module/payment_result.html',
                          {'error': e_message})
    else:
        return HttpResponse('پرداخت با خطا مواجه شد یا توسط شما کنسل شد')
