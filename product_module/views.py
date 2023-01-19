from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from site_module.models import SiteBanner
from utils.http_service import get_client_ip
from utils.convertors import group_list
from .models import Product, ProductCategory, ProductBrand, ProductVisit, ProductGallery, ProductComment


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'product'
    ordering = ['-created', '-price']
    paginate_by = 10


    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        query = Product.objects.all()
        product: Product = query.order_by('-price').first()
        db_max_price = product.price if product is not None else 0
        context['db_max_price'] = db_max_price
        context['start_price'] = self.request.GET.get('start_price') or 0
        context['end_price'] = self.request.GET.get('end_price') or db_max_price
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_list)

        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        request: HttpRequest = self.request
        start_price = request.GET.get('start_price')
        end_price = request.GET.get('end_price')
        if start_price is not None:
            query = query.filter(price__gte=start_price)

        if end_price is not None:
            query = query.filter(price__lte=end_price)

        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
        elif brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name)
        data = query.filter(is_active=True)
        return data


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        requests = self.request.session
        favorite_product_id = self.request.session.get("product_favorite")
        context["is_favorite"] = favorite_product_id == str(loaded_product.id)
        context['banners'] = SiteBanner.objects.filter(is_active=True,
                                                       position__iexact=SiteBanner.SiteBannerPosition.product_detail)
        galeries = list(ProductGallery.objects.filter(product_id=loaded_product.id).all())
        galeries.insert(0, loaded_product)
        context['product_galleries_group'] = list(group_list(galeries, 3))
        context['related_products'] = list(
            group_list(
                Product.objects.filter(brand_id=loaded_product.brand_id).exclude(pk=loaded_product.id).all()[:12], 3))
        # Get user IP address for viewing product
        user_ip = get_client_ip(self.request)
        user_id = None
        # Check user id in product views
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ProductVisit.objects.filter(ip__exact=user_ip, product_id=loaded_product.id).exists()
        if not has_been_visited:
            new_visit = ProductVisit(ip=user_ip, user_id=user_id, product_id=loaded_product.id)
            new_visit.save()

        product: Product = kwargs.get('object')
        context['comment'] = ProductComment.objects.filter(product_id=product.id, parent=None).order_by(
            '-created').prefetch_related(
            'productcomment_set')
        context['comment_count'] = ProductComment.objects.filter(product_id=product.id).count()
        return context


def product_categories_component(request):
    product_main_categories = ProductCategory.objects.annotate(
        products_count=Count('product_categories')).prefetch_related(
        'productcategory_set').filter(
        is_active=True, is_delete=False, parent_id=None)
    context = {
        'main_categories': product_main_categories
    }
    return render(request, 'product_module/components/product_categories_component.html', context)


def product_brands_component(request):
    product_brand = ProductBrand.objects.annotate(products_count=Count('product')).filter(is_active=True)
    context = {
        'brands': product_brand
    }
    return render(request, 'product_module/components/product_brands_component.html', context)


def add_product_comment(request):
    if request.user.is_authenticated:
        product_comment = request.GET.get('product_comment')
        product_id = request.GET.get('product_id')
        parent_id = request.GET.get('parent_id')
        print(product_comment, product_id, parent_id)
        new_comment = ProductComment(product_id=product_id, text=product_comment, user_id=request.user.id,
                                     parent_id=parent_id)
        new_comment.save()
        context = {
            'comment': ProductComment.objects.filter(product_id=product_id, parent=None).order_by(
                '-created').prefetch_related(
                'productcomment_set'),
            'comment_count': ProductComment.objects.filter(product_id=product_id).count()
        }
        return render(request, 'product_module/includes/product_comment_partial.html', context)
    return HttpResponse('hello')
