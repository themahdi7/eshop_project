from django.urls import path, re_path
from . import views

app_name = "product"
urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brands_list'),
    path('add-product-comment', views.add_product_comment, name='add_product_comment'),
    re_path('(?P<pk>[-\w]+)/(?P<slug>[-\w]+)', views.ProductDetailView.as_view(), name="product_detail"),
]
