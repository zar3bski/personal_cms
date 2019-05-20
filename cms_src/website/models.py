from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from datetime import datetime

'''Tweaks and tricks'''
def get_name(self):
    return "{} {}".format(self.first_name, self.last_name)

User.add_to_class("__str__", get_name)

class SingletonModel(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
            self.pk = 1
            super(SingletonModel, self).save(*args, **kwargs)
            self.set_cache()
    
    def delete(self, *args, **kwargs):
        pass

    @classmethod
    def load(cls):
        if cache.get(cls.__name__) is None:
            obj, created = cls.objects.get_or_create(pk=1)
            if not created:
                obj.set_cache()
        return cache.get(cls.__name__)

    def set_cache(self):
        cache.set(self.__class__.__name__, self)

'''                               MODELS'''
class SiteSetting(SingletonModel):
    title            = models.CharField(max_length=100,default='my_site_title')
    about            = models.TextField()
    owner_first_name = models.CharField(max_length=100,default='my_first_name')
    owner_last_name  = models.CharField(max_length=100,default='my_last_name')

'''                               categorical models'''
class Category(models.Model):
    parent        = models.ForeignKey('self', default=None, null=True, blank=True, related_name='nested_category', on_delete=models.CASCADE)
    name          = models.CharField(max_length=50, unique=True)
    nesting_level = models.IntegerField(default = 0, validators = [MaxValueValidator(3)], help_text="Leave it how it is. The app takes care of everything")
    slug          = models.SlugField(max_length=60, allow_unicode=True)

    def __init__(self, *args, **kwargs): 
        super(Category, self).__init__(*args, **kwargs)
        if self.parent != None:
            self.nesting_level = self.parent.nesting_level + 1
        elif self.parent == None:
            self.nesting_level = 0

    class Meta:
        unique_together = ('slug', 'parent',) 
        verbose_name_plural = "categories"       

    def __str__(self):                           
        full_path = [self.name.lower()]                                        
        k = self.parent                          

        while k is not None:
            full_path.append(k.name.lower())
            k = k.parent

        return '->'.join(full_path[::-1])

    # TODO mettre en cache
    @classmethod
    def load(cls):
        _categories = cls.objects.all()
        nav_tree = [{"name":x.name, "slug":x.slug, "id":x.id, "path":str(x), "children": [{"name":y.name, "slug":y.slug, "id":y.id, "path":str(y)} for y in _categories if y.parent==x]} for x in _categories if x.nesting_level == 0]
        
        return nav_tree

'''                               editorial models'''
class Publication(models.Model):
    date    = models.DateField('date published')
    typeof  = models.CharField(max_length=20)
    journal = models.CharField(max_length=100)
    editor  = models.CharField(max_length=100)
    link    = models.URLField(null=True)

class Article(models.Model):
    first_written = models.DateField(auto_now_add=True)
    last_udate    = models.DateField('date published')
    tags          = models.CharField(max_length=100, help_text="comma separated tags")
    title         = models.CharField(max_length=100)
    visible       = models.BooleanField(default=True)
    content       = models.TextField()
    category      = models.ForeignKey(Category, default="Misc", on_delete=models.SET_DEFAULT)
    language      = models.CharField(max_length=1 ,choices=[("fr","French"),("en", "English"),("es", "Spanish")], default="en")
    #rating        = models.PositiveSmallIntegerField()
    author        = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return self.title
    # TODO order by rating 
    class Meta:
        ordering = ('last_udate',)

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

    def __str__(self): 
        return "{} _ {}".format(self.title, self.year)

class Diplome(Timeline):
    class Meta:
        verbose_name_plural = "diploma"

class Certification(Timeline):
    expire = models.DateField(null=True, blank=True)

class Job(models.Model):
    name         = models.CharField(max_length=100)
    year         = models.DateField('date started')
    duration     = models.DurationField()
    job_type     = models.CharField(max_length=100)
    compagny     = models.CharField(max_length=100)
    compagny_url = models.URLField(null=True)
    decription   = models.TextField(null=True)

        
class Project(models.Model):
    name        = models.CharField(max_length=100)
    url         = models.URLField()
    description = models.TextField()

