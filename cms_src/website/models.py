from django.db import models
from django.core.cache import cache
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, int_list_validator
from datetime import datetime
from mptt.models import MPTTModel, TreeForeignKey

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
'''
class Category(MPTTModel): 
    name   = models.CharField(max_length=50, unique=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class MPTTMeta:
        order_insertion_by = ['name']
        verbose_name_plural = "categories"

    @classmethod
    def load(cls):
        pass
'''
class Category(models.Model):
    parent        = models.ForeignKey('self', default=None, null=True, blank=True, related_name='nested_category', on_delete=models.CASCADE)
    name          = models.CharField(max_length=50, unique=True)
    nesting_level = models.IntegerField(default = 0, editable=False)
    slug          = models.SlugField(max_length=60, allow_unicode=True)
    cluster       = models.CharField(default = "", max_length=20, editable=False)
    path          = models.CharField(default = "", max_length=50, editable=False)


    def save(self, *args, **kwargs):
        if self.parent != None:
            self.nesting_level = self.parent.nesting_level + 1
            self.parent.cluster = "{},{}".format(self.parent.cluster,self.id)
        elif self.parent == None:
            self.nesting_level = 0
        self.path = str(self)
        print("mon id: {}({}), mon cluster: {}({})".format(self.id, type(self.id), self.cluster, type(self.cluster)))
        super(Category, self).save(*args, **kwargs)
    

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
        nav_tree = [{"name":x.name,"id":x.id,"path":str(x), "children": [{"name":y.name, "id":y.id, "path":str(y)} for y in _categories if y.parent==x]} for x in _categories if x.parent == None]
        
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
    last_update   = models.DateField('date published')
    tags          = models.CharField(max_length=100, help_text="comma separated tags")
    title         = models.CharField(max_length=100)
    visible       = models.BooleanField(default=True)
    content       = models.TextField()
    category      = models.ForeignKey(Category, default="Misc", on_delete=models.SET_DEFAULT)
    language      = models.CharField(max_length=2 ,choices=[("fr","French"),("en", "English"),("es", "Spanish")], default="en")
    rating        = models.PositiveSmallIntegerField(default= 0, editable=False)
    author        = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)


    def __str__(self):
        return self.title
    # TODO order by rating 
    class Meta:
        ordering = ('last_update','rating')

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

