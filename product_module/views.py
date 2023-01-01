from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from .models import Product


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'product'
    ordering = ['-created', '-price']
    paginate_by = 1

    def get_queryset(self):
        base_query = super(ProductListView, self).get_queryset()
        data = base_query.filter(is_active=True)
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
        return context


class AddProductFavorite(View):
    """
    save product in session for favorite list
    """
    def post(self, request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)
        request.session['product_favorite'] = product_id
        return redirect(product.get_absolute_url())
