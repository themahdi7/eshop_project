from django import forms
from django.core.exceptions import ValidationError

from account_module.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام خانوادگی',
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control',
                'placeholder': 'تصویر نمایه',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'آدرس',
                'rows': '5',
            }),
            'about_user': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'درباره من',
                'rows': '5',
            }),
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'رمز عبور قبلی'})
    )
    new_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 'placeholder': 'رمز عبور جدید'})
    )
    confirm_new_password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'تکرار رمز عبور'})
    )

    def clean_confirm_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        confirm_new_password = self.cleaned_data.get('confirm_new_password')

        if new_password == confirm_new_password:
            return confirm_new_password
        raise ValidationError('رمز عبور با تکرار رمز عبور مغایرت دارد')
