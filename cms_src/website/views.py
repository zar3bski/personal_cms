from django.shortcuts import render
from django.views import View
from django.template import loader
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from .models import SiteSetting, Diplome, Certification, Article, Category
from .forms import BrowseForm
from django.contrib import admin

class Home(View):
    template = loader.get_template("website/home.html")
    def get(self, request):
        print(request)
        context = {}
        return HttpResponse(self.template.render(context, request))

class Browse(View):
    template = loader.get_template("website/browse.html")
         
    def get(self, request):
        q_args = {q.split("=")[0]:q.split("=")[1] for q in request.GET.urlencode().split("&")}

        order_mode = q_args.get("order_mode", "last_update")
        page = int(q_args.get("page", "1"))
        root = Category.objects.get(id=q_args["category"])
        nav_form = BrowseForm(root.id, order_mode)     
        breadcrumb = root.path.split('->')

        cat      = Category.objects.filter(path__startswith=root.path).values_list('id', flat=True)
        articles = Article.objects.filter(category__in=cat).order_by("-"+order_mode)[(page-1)*5:(page-1)*5+5]

        for a in articles: 
            a.tags    = a.tags.split(',')
            a.content = a.content[0:400]

        context  = {"breadcrumb": breadcrumb, "articles": articles, "page": page, "order_mode": order_mode, 
        "nav_form": nav_form}
        return HttpResponse(self.template.render(context, request))

class Education(View):
    template = loader.get_template("website/education.html")

    def get(self, request):
        diploma        = Diplome.objects.all().order_by('-year')
        certifications = Certification.objects.all().order_by('-year')
        context        = {"diploma": diploma, "certifications":certifications}
        return HttpResponse(self.template.render(context, request))
