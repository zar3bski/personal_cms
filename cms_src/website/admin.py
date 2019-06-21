from django import forms
from django.contrib import admin
from .models import *
from personal_cms.widgets import CssEditor

class DesignForm(forms.ModelForm):
    model = UserDesign
    class Meta:
        fields = '__all__'
        widgets = {
            'code': CssEditor(attrs={'style': 'width: 90%; height: 100%;'}),
        }
        initial ={
        	'code': UserDesign.objects.first()
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

admin.site.register(UserDesign, DesignFormAdmin)
