from django.db.models import Count, Sum
from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from utils.convertors import group_list
from site_module.models import SiteSetting, FooterLinkBox, Slider, SiteBanner
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

        # order by latest products on homepage
        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-created')[:12]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]
        context['latest_products'] = group_list(latest_products, 4)

        # order by most visit products on homepage
        context['most_visit_products'] = group_list(most_visit_products, 4)
        categories = list(
            ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True,
                                                                                               is_delete=False,
                                                                                               product_count__gt=1)[:6])
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4]),
            }
            categories_products.append(item)
        context['categories_products'] = categories_products

        # order by most bought products on homepage
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(order_count=Sum(
            'orderdetail__count'
        )).order_by('-order_count')
        context['most_bought_products'] = group_list(most_bought_products)[:12]

        return context


class AboutUsView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutUsView, self).get_context_data(**kwargs)
        setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = setting
        return context


class ProductSearchView(ListView):
    template_name = 'home_module/product_search_result.html'
    model = Product
    context_object_name = 'product'
    ordering = ['-created', '-price']
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        q = request.GET.get('q')
        self.result = Product.objects.filter(title__contains=q, is_active=True,
                                             is_delete=False).order_by('-price').all()
        print(self.result)
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(ProductSearchView, self).get_context_data()
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_list)
        context['result'] = self.result
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
