from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import TemplateView
from account_module.models import User
from order_module.models import Order, OrderDetail
from user_panel_module.forms import EditProfileForm, ChangePasswordForm


@method_decorator(login_required, name='dispatch')
class UserPanelDashboardView(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard.html'


@method_decorator(login_required, name='dispatch')
class EditUserProfilePage(View):
    template_name = 'user_panel_module/edit_profile_page.html'

    def get(self, request, *args, **kwargs):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(instance=current_user)
        context = {
            'form': edit_form,
            'user': current_user,
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileForm(request.POST, request.FILES, instance=current_user)
        edit_form.save(commit=True)
        context = {
            'form': edit_form,
            'user': current_user,
        }
        return render(request, self.template_name, context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordPage(View):
    template_name = 'user_panel_module/change_password_page.html'

    def get(self, request):
        context = {
            'form': ChangePasswordForm(),
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            current_password = form.cleaned_data.get('current_password')
            new_password = form.cleaned_data.get('new_password')
            if current_user.check_password(current_password):
                if current_password == new_password:
                    form.add_error('new_password', 'کلمه عبور تکراری است')
                else:
                    current_user.set_password(new_password)
                    current_user.save()
                    return redirect(reverse('panel:user_dashboard'))
            else:
                form.add_error('current_password', 'کلمه عبور وارد شده اشتباه میباشد')

        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


def user_panel_menu_component(request):
    return render(request, 'component/user_panel_menu_component.html', {})


@method_decorator(login_required, name='dispatch')
class UserBasketPage(TemplateView):
    template_name = 'user_panel_module/user_basket.html'

    def get_context_data(self, **kwargs):
        context = super(UserBasketPage, self).get_context_data(**kwargs)
        current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(
            is_paid=False, user_id=self.request.user.id)
        total_amount = current_order.calculate_amount()
        context = {
            'order': current_order,
            'sum': total_amount,
        }
        return context


def remove_order_content(request):
    detail_id = request.GET.get('detail_id')
    if detail_id is None:
        return JsonResponse({
            'status': 'not_found_detail_id'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(
        id=detail_id, order__is_paid=False, order__user__id=request.user.id).delete()

    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found',
            'title': 'خطا',
            'text': 'محصولی یافت نشد',
            'icon': 'erorr',
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(
        is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_amount()
    context = {
        'order': current_order,
        'sum': total_amount,
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context),
        'title': 'حذف شد',
        'text': 'محصول با موفقیت از سبد خرید حذف شد',
        'icon': 'success',
    })


def change_order_content(request):
    detail_id = request.GET.get('detail_id')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state_id'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()
    if order_detail is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    if state == 'increase':
        order_detail.count += 1
        if order_detail.count <= 1:
            order_detail.count = 1
            order_detail.save()

        order_detail.save()

    elif state == 'decrease':
        order_detail.count -= 1
        if order_detail.count <= 0:
            order_detail.count = 1
            order_detail.save()

        order_detail.save()

    else:
        return JsonResponse({
            'status': 'state_invalid'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(
        is_paid=False, user_id=request.user.id)
    total_amount = current_order.calculate_amount()
    context = {
        'order': current_order,
        'sum': total_amount,
    }
    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket_content.html', context),
        'title': 'حذف شد',
        'text': 'محصول با موفقیت از سبد خرید حذف شد',
        'icon': 'success',
    })
