from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from .models import User
from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_service import send_email


class RegisterView(View):
    template_name = 'account_module/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home:home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email_active_code = get_random_string(100)
            user_email = register_form.cleaned_data.get('email')
            user_password = register_form.cleaned_data.get('password')
            check_user: bool = User.objects.filter(email__iexact=user_email)
            if check_user:
                register_form.add_error('email', 'ایمیل وارد شده قبلا در سایت ثبت شده است')
            else:
                request.session['user_registration_info'] = {
                    'email': user_email,
                    'password': user_password,
                }
                user_session = request.session['user_registration_info']
                user_email = user_session['email']
                print(user_email)
                send_email('فعالسازی حساب کاربری', user_email, {'active': email_active_code, 'user': user_email},
                           'emails/activate_account.html')
                print("sent")
                return redirect(reverse('account:login_page'))

        context = {
            'register_form': register_form,
        }
        return render(request, self.template_name, context)


class ActivateAccountView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home:home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, email_active_code):
        print('activate_account')
        user_session = request.session['user_registration_info']
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is None:
            new_user = User(
                email=user_session['email'],
                email_active_code=email_active_code,
                is_active=True,
                username=user_session['email'],
            )
            new_user.set_password(user_session['password'])
            new_user.email_active_code = get_random_string(100)
            new_user.save()

            return redirect(reverse('account:login_page'))
            # else:
            #     # todo : show error
            #     pass
        else:
            raise Http404


class LoginView(View):
    template_name = 'account_module/login.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('home:home'))
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form,
        }
        return render(request, self.template_name, context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('password', 'حساب کاربری شما فعال نیست')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home:home'))
                    else:
                        login_form.add_error('password', 'نام کاربری یا کلمه عبور اشتباه است')
            else:
                login_form.add_error('password', 'نام کاربری یا کلمه عبور اشتباه است')

        context = {
            'login_form': login_form,
        }
        return render(request, self.template_name, context)


class ForgetPassword(View):
    template_name = 'account_module/forgot_password.html'

    def get(self, request):
        forget_pass_form = ForgotPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        forget_pass_form = ForgotPasswordForm(request.POST)
        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی رمز عبور', user_email, {'user': user},
                           'emails/forget_pass.html')


        context = {
            'forget_pass_form': forget_pass_form,
        }
        return render(request, self.template_name, context)


class ResetPassword(View):
    template_name = 'account_module/reset_password.html'

    def get(self, request, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            raise Http404
            # return redirect(reverse('account:login_page'))
        else:
            reset_pass_form = ResetPasswordForm()
            context = {
                'reset_pass_form': reset_pass_form,
                'user': user,
            }
            return render(request, self.template_name, context)

    def post(self, request, active_code):
        reset_pass_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_pass_form.is_valid():
            if user is None:
                return redirect(reverse('account:login_page'))
            else:
                user_new_pass = reset_pass_form.cleaned_data.get('password')
                user.set_password(user_new_pass)
                user.email_active_code = get_random_string(100)
                user.is_active = True
                user.save()
                return redirect(reverse('account:login_page'))


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('account:login_page'))
