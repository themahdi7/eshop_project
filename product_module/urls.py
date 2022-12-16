from django.urls import path
from . import views


urlpatterns = [
    path('', views.product_list, name="product_list"),
    path('<int:id>', views.product_detail, name="product_detail"),
]
