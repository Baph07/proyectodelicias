from django.urls import path
from .views import ingresos

urlpatterns = [
    path('', ingresos, name='ingresos'),
]