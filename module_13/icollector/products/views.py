from django.views.generic.base import TemplateView
from common.views import TitleMixin


class IndexView(TitleMixin, TemplateView):
    title = 'Home - iCollector'
    template_name = 'products/index.html'
