from .models import SiteSetting, Category
from django.core.cache import cache

def settings(request):
    return {'settings': SiteSetting.load(),
    		'article_categories': cache.get('Article_category'),
    		'photo_categories': cache.get('Photo_category')
    		}