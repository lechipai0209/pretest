from django.contrib import admin
from django.urls import path
from api.views import import_order, health_check

urlpatterns = [
    path('import-order/', import_order),
    path('import-product/', import_product),
    path('health-check/', health_check),
]