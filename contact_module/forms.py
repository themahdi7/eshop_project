from django import forms
from .models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['title', 'email', 'full_name', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'نام و نام خانوادگی',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'ایمیل',
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'عنوان',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'متن پیام',
                'rows': '8',
                'id': 'message'
            })
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام و نام خانوادگی خود وارد کنید',
            },
            'email': {
                'required': 'لطفا ایمیل خود وارد کنید',
            },
            'title': {
                'required': 'لطفا عنوان پیام خود وارد کنید',
            },
            'message': {
                'required': 'لطفا پیام خود وارد کنید',
            }
        }

