from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('foreCast/<str:city>', views.foreCast, name='foreCast'),
]