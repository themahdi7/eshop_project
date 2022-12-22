from django.urls import path
from . import views

app_name = "home"
urlpatterns = [
    path('', views.index_page, name='home'),
    path('contact-us', views.contact_page, name='contact_us'),
]
