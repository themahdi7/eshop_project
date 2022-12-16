from django.shortcuts import render, get_object_or_404
from .models import Product
from django.http import Http404


def product_list(request):
    products = Product.objects.all()
    return render(request, 'product_module/product_list.html', {'product': products})


def product_detail(request, id):
    product = get_object_or_404(Product, pk=id)
    return render(request, 'product_module/product_detail.html', {
        'product': product
    })

