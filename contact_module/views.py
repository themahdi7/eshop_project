from django.shortcuts import render


def contact_page(request):
    return render(request, 'contact_module/contact_page.html')
