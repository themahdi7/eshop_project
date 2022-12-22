from django.shortcuts import render


def index_page(request):
    return render(request, 'home_module/index_page.html')


def site_header_component(request):
    return render(request, 'shared/site_header_component.html', {})


def site_footer_component(request):
    return render(request, 'shared/site_footer_component.html', {})
