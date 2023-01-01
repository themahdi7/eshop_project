from django.urls import path
from . import views

app_name = "contact"
urlpatterns = [
    path('', views.ContactUsView.as_view(), name="contact_page"),
    path('profile', views.CreateProfileView.as_view(), name="profile_page"),
    path('profiles', views.ProfileView.as_view(), name="profiles-list"),
]

