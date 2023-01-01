from django import forms
from django.core import validators
from django.core.exceptions import ValidationError


# class RegisterForm(forms.ModelForm):
#     password = forms.CharField(
#         min_length=8,
#         label='تکرار رمز عبور',
#         widget=forms.PasswordInput({'placeholder': 'رمز عبور'})
#     )
#     confirm_password = forms.CharField(
#         min_length=8,
#         label='تکرار رمز عبور',
#         widget=forms.PasswordInput({'placeholder': 'تکرار رمز عبور'})
#     )
#
#     class Meta:
#         model = User
#         fields = ['email']
#         widgets = {
#             'email': forms.EmailInput(attrs={
#                 'placeholder': 'ایمیل',
#             }),
#         }
#
#     def clean_confirm_password(self):
#         password = self.cleaned_data.get('password')
#         confirm_password = self.cleaned_data.get('confirm_password')
#         if password == confirm_password:
#             return confirm_password
#         raise ValidationError('رمز عبور با تکرار رمز عبور مغایرت دارد')
#
#     def save(self, commit=True):
#         user = super(RegisterForm, self).save(commit=False)
#         if commit:
#             user.save()
#         return user
# return super(RegisterForm, self).save(commit=commit)

class RegisterForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput({'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator,

        ]
    )
    password = forms.CharField(
        min_length=8,
        label='رمز عبور',
        widget=forms.PasswordInput({'placeholder': 'رمز عبور'})
    )

    confirm_password = forms.CharField(
        min_length=8,
        label='تکرار رمز عبور',
        widget=forms.PasswordInput({'placeholder': 'تکرار رمز عبور'})
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password == confirm_password:
            return confirm_password
        raise ValidationError('رمز عبور با تکرار رمز عبور مغایرت دارد')


class LoginForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput({'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        min_length=8,
        label='رمز عبور',
        widget=forms.PasswordInput({'placeholder': 'رمز عبور'})
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        max_length=100,
        label='ایمیل',
        widget=forms.EmailInput({'placeholder': 'ایمیل'}),
        validators=[
            validators.EmailValidator,
        ]
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        min_length=8,
        label='رمز عبور',
        widget=forms.PasswordInput({'placeholder': 'رمز عبور'})
    )
    confirm_password = forms.CharField(
        min_length=8,
        label='تکرار رمز عبور',
        widget=forms.PasswordInput({'placeholder': 'تکرار رمز عبور'})
    )

