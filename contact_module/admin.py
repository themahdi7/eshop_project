from django.contrib import admin
from django.contrib import messages
from . import models
from .models import ContactUs


# @admin.register(models.ContactUs)

class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['title', 'full_name', 'email', 'is_read_by_admin', 'send_email']
    list_filter = ['email', 'is_read_by_admin', 'send_email', 'title', 'full_name', ]

    def save_model(self, request, obj: ContactUs, form, change):
        if obj.is_read_by_admin and obj.response and not obj.send_email:
            messages.add_message(request, messages.INFO, f'ایمیل پاسخ به "{obj.full_name}" با موفقیت ارسال شد')
        super(ContactUsAdmin, self).save_model(request, obj, form, change)

admin.site.register(models.ContactUs, ContactUsAdmin)
