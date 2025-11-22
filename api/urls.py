from django.contrib import admin
from django.urls import path
from api.views import import_order, health_check, import_product, get_orders, get_products

urlpatterns = [
    path('import-order/', import_order),
    path('import-product/', import_product),
    path('health-check/', health_check),
    path('get-orders/', get_orders),
    path('get-products/', get_products),
]