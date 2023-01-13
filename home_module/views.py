from django.db.models import Count
from django.shortcuts import render
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from utils.convertors import group_list
from site_module.models import SiteSetting, FooterLinkBox, Slider
from utils.http_service import get_client_ip


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slider = Slider.objects.filter(is_active=True).all()
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = {
            'slider': slider,
            'site_setting': setting
        }
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-created')[:12]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products, 4)
        context['most_visit_products'] = group_list(most_visit_products, 4)
        categories = list(ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True, is_delete=False, product_count__gt=1)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4]),
            }
            categories_products.append(item)
        context['categories_products'] = categories_products

        return context


class AboutUsView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context


def site_header_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': setting
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.filter(is_active=True)

    context = {
        'site_setting': setting,
        'footer_link_boxes': footer_link_boxes
    }
    return render(request, 'shared/site_footer_component.html', context)
