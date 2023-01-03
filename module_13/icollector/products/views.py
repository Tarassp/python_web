from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from common.views import TitleMixin
from .models import Product, ProductCategory


class IndexView(TitleMixin, TemplateView):
    title = 'Home - iCollector'
    template_name = 'products/index.html'


class ProductListView(TitleMixin, ListView):
    title = 'Products - iCollector'
    template_name = 'products/products.html'
    model = Product
    paginate_by = 6

    def get_queryset(self):
        queryset = super().get_queryset()
        category_id = self.kwargs.get('category_id')
        queryset = Product.objects.filter(category_id=category_id) if category_id else queryset
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ProductCategory.objects.all()
        return context


def basket_add(request):
    ...

