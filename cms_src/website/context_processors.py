from .models import SiteSetting, Category

def settings(request):
    return {'settings': SiteSetting.load(),
    		'categories': Category.load()
    		}