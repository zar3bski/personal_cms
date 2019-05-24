from django.urls import path

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browse/', views.Browse.as_view(), name='browse'),
    path('education/', views.Education.as_view(), name='education'),
]