from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Article_category, Photo_category, Person, Photo, Article
from django.contrib.auth.models import User
from django.core.cache import cache
from django.db.models import F

@receiver(post_save, sender=Photo_category)
@receiver(post_delete, sender=Photo_category)
@receiver(post_save, sender=Article_category)
@receiver(post_delete, sender=Article_category)
def refresh_cached_category(sender, instance, using, **kwargs):
    cache.set('{}'.format(sender.__name__), sender.objects.all())

@receiver(post_save, sender=Article)
@receiver(post_save, sender=Photo)
def add_one_to_count(sender, instance, **kwargs):
    instance.category.count = F('count')+1
    instance.category.save()
    cache.set('{}_category'.format(sender.__name__), type(instance.category).objects.all())

@receiver(post_delete, sender=Article)
@receiver(post_delete, sender=Photo)
def drop_one_to_count(sender, instance, **kwargs):
    instance.category.count = F('count')-1
    instance.category.save()    
    cache.set('{}_category'.format(sender.__name__), type(instance.category).objects.all())

@receiver(post_save, sender=User)
def add_new_user_to_persons(sender, instance, **kwargs): 
    p = Person.objects.get_or_create(
        first_name = instance.first_name, 
        last_name  = instance.last_name)
    