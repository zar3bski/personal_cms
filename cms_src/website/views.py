from django.shortcuts import render
from django.views import View
from django.template import loader
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import SiteSetting, Diplome, Certification, Article, Category
from django.contrib import admin

categories = Category.load()

class Home(View):
    template = loader.get_template("website/home.html")
    def get(self, request):
        print(request)
        context = {}
        return HttpResponse(self.template.render(context, request))

class Browse(View):
    template = loader.get_template("website/browse.html")
    def get(self, request, category, order_mode="time" , page=1):
        print(category)
        print(categories)

        #TODO extraite l'id correspondant à la category pour trouver toutes les catégories filles afin de filtrer les articles
        print(categories["path"==category])
        print(categories["path"==category]["id"])
        #print(entry.__dict__)
        path = category.split('->')
        #articles = Article.objects.filter(category=entry)
        articles = Article.objects.all()
        for a in articles: 
            a.tags    = a.tags.split(',')
            a.content = a.content[0:400]

        context  = {"path": path, "articles": articles}
        return HttpResponse(self.template.render(context, request))

class Education(View):
    template = loader.get_template("website/education.html")

    def get(self, request):
        diploma        = Diplome.objects.all().order_by('-year')
        certifications = Certification.objects.all().order_by('-year')
        context        = {"diploma": diploma, "certifications":certifications}
        return HttpResponse(self.template.render(context, request))
