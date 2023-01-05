from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="products"),
    path("baskets/add/<int:product_id>/", views.basket_add, name="basket_add"),
    path("baskets/remove/<int:basket_id>/", views.basket_remove, name="basket_remove"),
    path("page/<int:page>", views.ProductListView.as_view(), name="paginator"),
    path("category/<int:category_id>/", views.ProductListView.as_view(), name="category"),
]