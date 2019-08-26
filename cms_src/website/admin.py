from django import forms
from django.contrib import admin
from .models import *
from personal_cms.widgets import CssEditor
from django.conf import settings

class DesignForm(forms.ModelForm):
    model = UserDesign
    class Meta:
        fields = '__all__'
        widgets = {
            'code': CssEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }
        initial ={
        	'code': open(settings.BASE_DIR+'/website/static/website/css/custom.css').read() or open(settings.BASE_DIR+'/website/static/website/css/custom-default.css').read()
        }

class DesignFormAdmin(admin.ModelAdmin):
    form = DesignForm


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
admin.site.register(Project)
admin.site.register(Job)

admin.site.register(UserDesign, DesignFormAdmin)
