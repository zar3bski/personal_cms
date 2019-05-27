from django.urls import path
from django.conf.urls import url
from django.http import HttpResponse

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browse/', views.Browse.as_view(), name='browse'),
    path('education/', views.Education.as_view(), name='education'),
    url(r'^read/(?P<path>[->\w]+)/(?P<article_id>[\d]+)/$', views.Reader.as_view(), name="reader"), 
    path('robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /admin", content_type="text/plain"), name="robots_file"),
]