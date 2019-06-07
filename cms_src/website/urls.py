from django.urls import path
from django.conf.urls import url
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('browse/<str:super_category>/', views.Browse.as_view(), name='browse'),
    path('gallery/<str:super_category>/', views.Gallery.as_view(), name='gallery'),
    path('thumb_up/<str:con_type>/<int:post_id>/', views.thumb_up, name="vote"),
    path('education/', views.Education.as_view(), name='education'),
    url(r'^read/(?P<path>[->\w]+)/(?P<article_id>[\d]+)/$', views.Reader.as_view(), name="reader"), 
    path('robots.txt', lambda x: HttpResponse("User-Agent: *\nDisallow: /admin", content_type="text/plain"), name="robots_file"),
]+ static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)