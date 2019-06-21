from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Article_category, Photo_category, Person, Photo, Article, ExternalAccount, SiteSetting, UserDesign
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import F
from django.conf import settings

@receiver(post_save, sender=ExternalAccount)
@receiver(post_delete, sender=ExternalAccount)
@receiver(post_save, sender=Photo_category)
@receiver(post_delete, sender=Photo_category)
@receiver(post_save, sender=Article_category)
@receiver(post_delete, sender=Article_category)
def refresh_cached_model(sender, instance, using, **kwargs):
    cache.set('{}'.format(sender.__name__), sender.objects.all(),None)

@receiver(post_save, sender=UserDesign)
@receiver(post_delete, sender=UserDesign)
@receiver(post_save, sender=SiteSetting)
@receiver(post_delete, sender=SiteSetting)
def refresh_cached_singleton(sender, instance, **kwargs):
    cache.set('{}'.format(sender.__name__), instance, None)
    
@receiver(post_save, sender=UserDesign)
@receiver(post_delete, sender=UserDesign)
def override_css(sender, instance, **kwargs):
    with open(settings.BASE_DIR+'/website/static/website/css/custom.css', "w") as css:
        css.write(instance.code)
    with open(settings.STATIC_ROOT+'/website/css/custom.css', "w") as css:
        css.write(instance.code)

@receiver(post_save, sender=Article)
@receiver(post_save, sender=Photo)
def add_one_to_count(sender, instance, **kwargs):
    instance.category.count = F('count')+1
    instance.category.save()
    cache.set('{}_category'.format(sender.__name__), type(instance.category).objects.all(),None)

@receiver(post_delete, sender=Article)
@receiver(post_delete, sender=Photo)
def drop_one_to_count(sender, instance, **kwargs):
    instance.category.count = F('count')-1
    instance.category.save()    
    cache.set('{}_category'.format(sender.__name__), type(instance.category).objects.all(),None)

@receiver(post_save, sender=User)
def add_new_user_to_persons(sender, instance, **kwargs): 
    p = Person.objects.get_or_create(
        first_name = instance.first_name, 
        last_name  = instance.last_name)
    