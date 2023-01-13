from django.urls import path
from . import views

app_name = "panel"
urlpatterns = [
    path('', views.UserPanelDashboardView.as_view(), name="user_dashboard"),
    path('edit-profile', views.EditUserProfilePage.as_view(), name="edit_profile"),
    path('change-password', views.ChangePasswordPage.as_view(), name="change_password"),
    path('user-order', views.UserBasketPage.as_view(), name="user_order_page"),
    path('remove-order-detail', views.remove_order_content, name="remove_order_detail"),
    path('change-order-detail', views.change_order_content, name="change_order_detail"),
]
