from django.db import models, connection
from django.core.cache import cache
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime
from abc import abstractmethod
from datetime import timedelta
from django.conf import settings
from django.db.models import Max
from random import randint

'''Tweaks and tricks'''
def get_name(self):
    return "{} {}".format(self.first_name, self.last_name)

User.add_to_class("__str__", get_name)

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    @abstractmethod
    def save(self, *args, **kwargs):
        self.pk = 1
        super(SingletonModel, self).save(*args, **kwargs)

    @classmethod
    def load(cls):
        if cls.objects.first() == None:
            data = {str(k).split('.')[-1]: k.get_default() for k in cls._meta.fields}
            s = cls(data)
            s.save()
        cache.set('{}'.format(cls.__name__), cls.objects.first(), None)

'''                               MODELS'''
class SiteSetting(SingletonModel):
    title             = models.CharField(max_length=100,default='my_site_title')
    about             = models.TextField(null=True, blank=True)
    keywords          = models.CharField(max_length=120, help_text="comma separated tags", null=True)
    url               = models.URLField(max_length=200, null=True, blank=True)
    profil_image      = models.ImageField(null=True, upload_to='photo', default="photo/profile_placeholder.png")
    owner_first_name  = models.CharField(max_length=100,default='my_first_name')
    owner_last_name   = models.CharField(max_length=100,default='my_last_name')
    bio               = models.TextField(max_length=800, help_text="markdown syntax", null=True, blank=True)
    display_bio       = models.BooleanField(default=False)
    display_skills    = models.BooleanField(default=False)
    display_carousel  = models.BooleanField(default=False)
    footer            = models.TextField(max_length=200,null=True, blank=True, help_text="markdown syntax")
    gallery_width     = models.PositiveSmallIntegerField(default=3, validators=[
                MinValueValidator(2), 
                MaxValueValidator(5)])
    nb_page_gallery   = models.PositiveSmallIntegerField(default=8, validators=[
                MinValueValidator(4), 
                MaxValueValidator(30)],
                help_text='number of items by gallery page')
    show_gallery        = models.BooleanField(default=False)
    show_articles       = models.BooleanField(default=False)
    show_projects       = models.BooleanField(default=False)
    show_education      = models.BooleanField(default=False)
    show_jobs           = models.BooleanField(default=False)
    show_certifications = models.BooleanField(default=False)

class UserDesign(SingletonModel): 
    name   = models.CharField(max_length=255, default="default")
    code   = models.TextField(default=open(settings.BASE_DIR+'/website/static/website/css/custom-default.css').read())
    
    def __unicode__(self):
        return self.name

class ExternalAccount(models.Model):
    plateform_name = models.CharField(max_length=60)
    url            = models.URLField()
    logo           = models.ImageField(upload_to='logo')
    @classmethod
    def load(cls):
        cache.set('{}'.format(cls.__name__), cls.objects.all(), None)

    def __str__(self): 
        return self.plateform_name

'''                               categorical models'''
class Category(models.Model):
    class Meta: 
        abstract = True

    parent = models.ForeignKey('self', null=True, blank=True, related_name='nested_category', on_delete=models.SET_NULL)
    name   = models.CharField(max_length=50)
    path   = models.CharField(default = "", max_length=50, editable=False)
    count  = models.PositiveSmallIntegerField(default=0, editable=False)

    @abstractmethod
    def save(self, *args, **kwargs):
        self.path = str(self)
        
        super(Category, self).save(*args, **kwargs) 

    @abstractmethod
    def __str__(self):                           
        full_path = [self.name.lower()]                                        
        k = self.parent                          
        while k is not None:
            full_path.append(k.name.lower())
            k = k.parent

        return '->'.join(full_path[::-1])

    @classmethod
    def load(cls):
        cache.set('{}'.format(cls.__name__), cls.objects.all(), None)

class Article_category(Category):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parent','name'], name='articlecatunicity')
        ]
        verbose_name_plural = "article_categories"

class Photo_category(Category):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parent','name'], name='photocatunicity')
        ] 
        verbose_name_plural = "photo_categories"
    visible_as_gallery = models.BooleanField(default=True)

'''                               editorial models'''
class Person(models.Model): 
    first_name = models.CharField(max_length=50, help_text="first name OR pseudo")
    last_name  = models.CharField(max_length=50, null=True, blank=True)
    url        = models.URLField(max_length=200, null=True, blank=True, unique=True)
    town       = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return "{} {}".format(self.first_name, self.last_name or "")

    class Meta:
        ordering = ['first_name']
        constraints = [
            models.UniqueConstraint(fields=['first_name','last_name'], name='personunicity')
        ]

class Post(models.Model): 
    class Meta:
        abstract        = True
        indexes         = [
            models.Index(fields=['category', 'nb_views', 'rating'])
        ] 
        constraints = [
            models.UniqueConstraint(fields=['title','author'], name='postunicity')
        ]


    title           = models.CharField(max_length=100)
    author          = models.ForeignKey(Person, null=True, on_delete=models.SET_NULL)
    rating          = models.PositiveSmallIntegerField(default=0, editable=False)
    nb_views        = models.PositiveIntegerField(default=0, editable=False)
    tags            = models.CharField(max_length=100, help_text="comma separated tags")
    family_friendly = models.BooleanField(default=True)
    description     = models.TextField(max_length=300, help_text="markdown syntax", null=True, blank=True)
    first_published = models.DateField(auto_now_add=True)

    @classmethod
    def get_random_instances(cls, nb=1, cat_list=None): 
        max_id = cls.objects.all().aggregate(max_id=Max("id"))['max_id'] or 1
        items  = []
        while len(items)<nb: 
            pk  = randint(1, max_id)
            item = cls.objects.filter(pk=pk).first()
            if item:
                if cat_list == None or item.category in cat_list: 
                    items.append(item)
        return items

# TODO: categories should be many to many relations
class Article(Post):
    category        = models.ForeignKey(Article_category, null=True, on_delete=models.SET_NULL)
    last_update     = models.DateField('date published')
    visible         = models.BooleanField(default=True)
    content         = models.TextField(help_text="markdown syntax. You can enable syntax highlighting in your fenced code by adding the typical extention of the language (e.g. ```py for python syntax)")
    photo           = models.ImageField(upload_to='article_photo', null=True, blank=True)
    language        = models.CharField(max_length=2 ,choices=[("fr","French"),("en", "English"),("es", "Spanish")], default="en")

    def __str__(self):
        return self.title
        
# TODO: categories should be many to many relations
class Photo(Post):
    category     = models.ForeignKey(Photo_category, null=True, on_delete=models.SET_NULL)
    photo_models = models.ManyToManyField(Person, related_name="models", blank=True)
    place_name   = models.CharField(max_length=100, null=True, blank=True)
    buy_link     = models.URLField(max_length=200, null=True, blank=True)
    photo        = models.ImageField(upload_to='photo')

    def __str__(self): 
        return "{} {} {}".format(self.author, self.place_name or "",self.id)

class Comment(models.Model):
    parent  = models.ForeignKey('self', default=None, null=True, blank=True, related_name='nested_comment', on_delete=models.CASCADE)
    date    = models.DateField(auto_now_add=True)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    content = models.TextField(max_length=300, help_text="markdown syntax")
    author  = models.CharField(max_length=100)
    rating  = models.PositiveSmallIntegerField(default=0, editable=False)

    def __str__(self):
        return "{}-{}-{}".format(self.author, self.date, self.content[:20])

    def __repr__(self): 
        return self

class Message(models.Model):
    date    = models.DateField(auto_now_add=True, editable=False)
    author  = models.CharField(max_length=100)
    mail    = models.EmailField()
    subject = models.CharField(max_length=120)
    content = models.TextField(max_length=500)

    def __str__(self):
        return "{}: {}".format(self.author, self.subject)

'''                               temporal models'''
class Timeline(models.Model): 
    year        = models.PositiveSmallIntegerField(blank=True, null=True, validators=[
                MinValueValidator(1900), 
                MaxValueValidator(datetime.now().year)])
    title       = models.CharField(max_length=100)
    institution = models.CharField(max_length=100)
    link        = models.URLField(null=True, blank=True)
    details     = models.TextField(null=True, blank=True, help_text="Use a Markdown syntax")

    class Meta:
        abstract = True
        ordering = ["-year"]

    def __str__(self): 
        return "{} _ {}".format(self.title, self.year)

class Diplome(Timeline):
    class Meta:
        verbose_name_plural = "diploma"

class Certification(Timeline):
    expire = models.DateField(null=True, blank=True)

class Job(Timeline):
    duration     = models.DurationField()
    job_type     = models.CharField(max_length=100)

    @property
    def duration_hrf(self): 
        t = self.duration.days
        if t > 365:
            return "{} Y {} M".format(t//365, int(t/365//30))
        elif 60< t <= 365:
            return "{} M {} W".format(t//30, int(t/30//7))
        elif 60 >= t:
            return "{} W".format(t//7)

class Project(models.Model):
    name        = models.CharField(max_length=100)
    url         = models.URLField()
    description = models.TextField(help_text="markdown syntax")
    image_url   = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.name

class Skill(models.Model): 
    name    = models.CharField(max_length=50)
    mastery = models.PositiveSmallIntegerField(validators=[
                MinValueValidator(1), 
                MaxValueValidator(100)])

    def __str__(self):
        return self.name