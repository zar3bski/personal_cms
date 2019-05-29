from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from .models import Category
from django.core.cache import cache

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def refresh_cached_category(sender, instance, using, **kwargs):
    cache.set('{}_categories'.format(instance.content_type), Category.objects.filter(content_type=instance.content_type))

'''
@receiver(post_save, sender=Category)
def delete_category(sender, instance, using, **kwargs):
    content_type = instance.content_type 
    cache.set('{}_categories'.format(content_type), Category.objects.filter(content_type=content_type))
'''