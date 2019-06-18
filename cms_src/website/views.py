from django.shortcuts import render, redirect
from django.views import View
from django.template import loader
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F, Max

from .models import SiteSetting, Diplome, Certification, Article, Article_category, Comment, Photo, Photo_category, Person, Skill
from .forms import BrowseForm, CommentForm, AddPictureForm, MessageForm
from .decorators import parse_q_args
from django.contrib import admin
from django.core.cache import cache
from django.apps import apps

from math import ceil
from random import randint

# TODO: this sucks!! uniform cache technique for this model with the rest of the cached model
settings = SiteSetting.load()

class Home(View):
    template     = loader.get_template("website/home.html")
    message_form = MessageForm
    
    def _get_random_pic(self,max_id): 
        while True: 
            pk  = randint(1, max_id)
            pic = Photo.objects.filter(pk=pk).first()
            if pic:
                return pic
    def get(self, request):
        context = {"message_form": self.message_form}

        if settings.display_carousel:
            max_id = Photo.objects.all().aggregate(max_id=Max("id"))['max_id']
            context["photos"] = [self._get_random_pic(max_id) for i in range(5)] 

        if settings.display_skills:
            context["skills"] = Skill.objects.all()

        return HttpResponse(self.template.render(context, request))

    def post(self, request): 
        message = self.message_form(request.POST)

        if message.is_valid():
            message.clean()
            message.save()

        return redirect(request.META['HTTP_REFERER'])

class Browse(View):
    template = loader.get_template("website/browse.html")
    
    @method_decorator(parse_q_args) 
    def get(self, request, super_category, order_mode="last_update", page=1):  
        breadcrumb = super_category.split('->')
        begin, end = (int(page)-1)*5,(int(page)-1)*5+5

        category_ids = cache.get('Article_category').filter(path__startswith=super_category.lower())
        articles = Article.objects.filter(category__in=category_ids).order_by("-"+order_mode)[begin:end]

        total_items = sum(c.count for c in category_ids)
        max_page = int(ceil(total_items / 5))

        for a in articles: 
            a.tags    = a.tags.split(',')
            a.content = a.content[0:400]

        context  = {"breadcrumb": breadcrumb, "articles": articles, "current_page": page, "max_page":max_page, "order_mode": order_mode}
        return HttpResponse(self.template.render(context, request))

class Reader(View):
    template = loader.get_template("website/article.html")
    comment_form = CommentForm

    def get(self, request, path, article_id): 
        article          = Article.objects.get(id=article_id)
        article.nb_views = F('nb_views')+1
        article.save()
        article.refresh_from_db()

        comments     = Comment.objects.select_related('article').filter(article_id=article_id)
        context      = {"article":article, "comment_form":self.comment_form, "comments":comments}
        return HttpResponse(self.template.render(context, request))

    def post(self, request, path, article_id): 
        comment = self.comment_form(request.POST)
        if comment.is_valid(): 
            comment.clean()
            try:
                parent = Comment.objects.get(id=comment["parent"].value())
            except ValueError:
                parent = None

            c = Comment.objects.create(
                author     = comment["author"].value(), 
                content    = comment["content"].value(),
                article_id = article_id, 
                parent     = parent)
            c.save()
            return redirect(request.META['HTTP_REFERER'])

class Timeline(View):
    template = loader.get_template("website/timeline.html")
    
    def get(self, request, model_name):
        model    = apps.get_model(app_label='website', model_name=model_name)
        timeline = model.objects.all()
        context  = {"model_name": model._meta.verbose_name_plural.title(), "timeline":timeline}
        return HttpResponse(self.template.render(context, request))

class Gallery(View): 
    template = loader.get_template("website/gallery.html")
    picture_form = AddPictureForm

    @method_decorator(parse_q_args)
    def get(self,request, super_category, page=1):
        item_range = settings.nb_page_gallery
        
        begin, end   = (int(page)-1)*item_range, (int(page)-1)*item_range + item_range
        category_ids = cache.get('Photo_category').filter(path__startswith=super_category.lower())
        photos       = Photo.objects.select_related('category').filter(category__in=category_ids)[begin:end]
        
        total_items  = sum(c.count for c in category_ids)
        max_page     = int(ceil(total_items / item_range))

        for p in photos: 
            p.tags   = p.tags.split(',')

        context      = {"photos":photos, "picture_form": self.picture_form, "current_page": page, "max_page":max_page}
        return HttpResponse(self.template.render(context, request))

    @method_decorator(login_required)
    def post(self,request, super_category):
        pic = self.picture_form(request.POST, request.FILES)
        
        if pic.is_valid(): 
            pic.clean()
            p = pic.save(commit=False)
            p.author       = Person.objects.get(id=pic["author"].value())
            p.category     = Photo_category.objects.get(name=super_category)

            p.save()
            pic.save_m2m()

            return redirect(request.META['HTTP_REFERER'])

def thumb_up(request, con_type, post_id): 
    form = request.POST
    print(form["upvote"])
    if form["upvote"] == "yes":
        if con_type == "article":
            Article.objects.filter(id=post_id).update(rating=F('rating')+1)
        elif con_type == "photo": 
            Photo.objects.filter(id=post_id).update(rating=F('rating')+1)
    return redirect(request.META['HTTP_REFERER'])
    