from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about-us', views.AboutUsView.as_view(), name='about_us_page'),
]
