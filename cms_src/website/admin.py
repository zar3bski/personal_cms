from django.contrib import admin
from .models import SiteSetting, Category, Diplome, Article, Certification, Comment, Photo, Person

admin.site.register(SiteSetting)
admin.site.register(Category)
admin.site.register(Diplome)
admin.site.register(Article)
admin.site.register(Certification)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Person)
