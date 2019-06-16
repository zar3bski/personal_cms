from .models import SiteSetting
from .forms import BrowseForm
from django.core.cache import cache

def settings(request):
    return {'settings': SiteSetting.load(),
    		'article_categories': cache.get('Article_category'),
    		'photo_categories': cache.get('Photo_category'), 
    		'external_accounts': cache.get('ExternalAccount'),
    		'nav_article_form': BrowseForm()
    		}