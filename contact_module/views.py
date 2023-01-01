from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.edit import CreateView

from site_module.models import SiteSetting
from .forms import ContactUsModelForm
from .models import UserProfile


class ContactUsView(CreateView):
    template_name = 'contact_module/contact_page.html'
    form_class = ContactUsModelForm
    success_url = reverse_lazy('contact:contact_page')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context


def store_file(file):
    with open('temp/image.jpg', 'wb+') as dest:
        for chunk in file.chunks():
            dest.write(chunk)


class CreateProfileView(CreateView):
    template_name = 'contact_module/create-profile.html'
    model = UserProfile
    fields = '__all__'
    success_url = reverse_lazy('contact:profile_page')


class ProfileView(ListView):
    model = UserProfile
    template_name = 'contact_module/profile-list.html'
    context_object_name = 'profiles'
