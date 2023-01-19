from django.urls import path, re_path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about-us', views.AboutUsView.as_view(), name='about_us_page'),
    path('search', views.ProductSearchView.as_view(), name='product_search_result'),
    # re_path('(?P<q>[-\w]+)', views.ProductSearchView.as_view(), name='product_search_page'),
]
