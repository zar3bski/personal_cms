from django.urls import path, re_path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    url(r'^browse/(?P<category>[->\w]+)/?(?P<order_mode>\w+)?/?(?P<page>\d+)?/$', views.Browse.as_view(), name='browse'),
    #re_path(r'^browse/<str:slug>/(?P<page>[0-9]{2})/$', views.Browse.as_view(), name='browse'),
    path('education/', views.Education.as_view(), name='education'),
]