from django.contrib import admin
from .models import SiteSetting, Article_category, Photo_category, Diplome, Article, Certification, Comment, Photo, Person, Skill, Message, ExternalAccount

#TODO: categorize to make navigation easier
admin.site.register(SiteSetting)
admin.site.register(Article_category)
admin.site.register(Photo_category)
admin.site.register(Diplome)
admin.site.register(Article)
admin.site.register(Certification)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Person)
admin.site.register(Skill)
admin.site.register(Message)
admin.site.register(ExternalAccount)
