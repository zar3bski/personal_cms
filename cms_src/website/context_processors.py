from .models import SiteSetting, Category
from django.core.cache import cache

def settings(request):
    return {'settings': SiteSetting.load(),
    		'article_categories': cache.get('article_categories'),
    		'photo_categories': cache.get('photo_categories')
    		}