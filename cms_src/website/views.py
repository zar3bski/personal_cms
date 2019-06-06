from django.shortcuts import render, redirect
from django.views import View
from django.template import loader
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.db.models import F

from .models import SiteSetting, Diplome, Certification, Article, Article_category, Comment, Photo, Photo_category, Person
from .forms import BrowseForm, CommentForm, AddPictureForm
from .decorators import parse_q_args
from django.contrib import admin
from django.core.cache import cache

from math import ceil

# TODO: this sucks!! uniform cache technique for this model with the rest of the cached models
settings = SiteSetting.load()

class Home(View):
    template = loader.get_template("website/home.html")
    def get(self, request):
        article_categories = cache.get('article_categories')
        print(article_categories)
        context = {}
        return HttpResponse(self.template.render(context, request))

class Browse(View):
    template = loader.get_template("website/browse.html")
         
    def get(self, request):
        q_args = {q.split("=")[0]:q.split("=")[1] for q in request.GET.urlencode().split("&")}

        order_mode = q_args.get("order_mode", "last_update")
        page       = int(q_args.get("page", "1"))
        root       = Article_category.objects.get(id=q_args["category"])
        nav_form   = BrowseForm(root.id, order_mode)     
        breadcrumb = root.path.split('->')

        cat      = Article_category.objects.filter(path__startswith=root.path).values_list('id', flat=True)
        articles = Article.objects.filter(category__in=cat).order_by("-"+order_mode)[(page-1)*5:(page-1)*5+5]

        for a in articles: 
            a.tags    = a.tags.split(',')
            a.content = a.content[0:400]

        context  = {"breadcrumb": breadcrumb, "articles": articles, "page": page, "order_mode": order_mode, 
        "nav_form": nav_form}
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

class Education(View):
    template = loader.get_template("website/education.html")

    def get(self, request):
        diploma        = Diplome.objects.all().order_by('-year')
        certifications = Certification.objects.all().order_by('-year')
        context        = {"diploma": diploma, "certifications":certifications}
        return HttpResponse(self.template.render(context, request))

class Gallery(View): 
    template = loader.get_template("website/gallery.html")
    picture_form = AddPictureForm

    @method_decorator(parse_q_args)
    def get(self,request, super_category, page=1):
        item_range = settings.nb_page_gallery
        # TODO: pagination . Cache number of pho
        begin, end = (int(page)-1)*item_range, (int(page)-1)*item_range + item_range
        category_ids = cache.get('Photo_category').filter(path__startswith=super_category.lower())
        photos       = Photo.objects.select_related('category').filter(category__in=category_ids)[begin:end]
        
        total_items = sum(c.count for c in category_ids)
        max_page = int(ceil(total_items / item_range))

        for p in photos: 
            p.tags         = p.tags.split(',')

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
    