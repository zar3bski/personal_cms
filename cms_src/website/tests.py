from django.test import RequestFactory, TestCase, Client
from django.core.cache import cache
from django.db.utils import IntegrityError

from .models import Article_category, Photo_category, Article, Person, Photo
from .views import Browse, Home

# TODO: integrate the following command in future CI pipeline : docker exec personal_cms_web_1 python manage.py test website

class TestCache(TestCase): 
	fixtures = ["config-1.yaml", "photo_categories.yaml", "article_categories.yaml", "external_accounts.yaml"]
		
	def test_cached_settings(self):
		self.assertTrue(cache.get('SiteSetting').show_projects == True)
		self.assertTrue(cache.get('SiteSetting').title == "My awsome site")
		self.assertTrue(cache.get('SiteSetting').url == "https://somewhere.overtherainbow.com")
		self.assertTrue(cache.get('SiteSetting').display_skills == True)

	def test_cached_categories(self):
		self.assertTrue(cache.get('Photo_category').count()==2)
		self.assertTrue(cache.get('Photo_category').get(pk=1).path=="landscape")
		self.assertTrue(cache.get('Photo_category').get(pk=2).name=="Portrait")

		self.assertTrue(cache.get('Article_category').count()==3)
		self.assertTrue(cache.get('Article_category').get(pk=1).path=="code")
		self.assertTrue(cache.get('Article_category').get(pk=1).parent==None)#
		self.assertTrue(cache.get('Article_category').get(pk=2).name=="Python")
		self.assertTrue(cache.get('Article_category').get(pk=2).path=="code->python")
		self.assertTrue(cache.get('Article_category').get(pk=2).parent==cache.get('Article_category').get(pk=1))

	def test_cached_external_accounts(self):
		self.assertTrue(cache.get('ExternalAccount').count()==2)
		self.assertTrue(cache.get('ExternalAccount').get(pk=1).plateform_name=="Facebook")
		self.assertTrue(cache.get('ExternalAccount').get(pk=2).url=="https://youtu.be/oavMtUWDBTM")
		self.assertTrue(cache.get('ExternalAccount').get(pk=2).logo=="logo/github.png")


'''VIEW TESTING'''
def setup_view(view, request, *args, **kwargs):
    """
    Mimic ``as_view()``, but returns view instance. Use this function to get view instances on which you can run unit tests, by testing specific methods.
    """
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view

class TestBrowseArticles(TestCase): 
	fixtures = ["article_categories.yaml", "person-1.yaml", "article-1.yaml"]

	def setUp(self):
		self.factory = RequestFactory()

	def test_data_retieval(self): 
		'''only articles under the browsed meta category and and children should be given'''
		request = self.factory.get('/browse/code/last_update')
		v = setup_view(Browse(), request)
		context = v._context_processor("code", "last_update", 1)

		self.assertTrue(len(context["articles"])==2)
		self.assertTrue(Article.objects.get(pk=1) in context["articles"])
		self.assertTrue(Article.objects.get(pk=2) in context["articles"])
		self.assertTrue(Article.objects.get(pk=3) not in context["articles"])	

#class TestViewHome(TestCase):
#	fixtures = ["config-1.yaml", "picture_categories.yaml", "article_categories.yaml", "external_accounts.yaml"] 

#	def setUp(self): 
#		self.factory = RequestFactory()

#	def test_biography_section(self): 
#		request  = self.factory.get("/")
#		response = Home.as_view()(request)
#		print(response)

'''MODEL TESTING'''

class TestCategoryModel(TestCase): 
	fixtures = ["photo_categories.yaml", "article_categories.yaml"]

	def test_category_creation(self): 
		x = Article_category.objects.create(parent=Article_category.objects.get(pk=1), name="DevOps")
		y = Photo_category.objects.create(parent=Photo_category.objects.get(pk=1), name="Nature")

		self.assertTrue(x.name == "DevOps")
		self.assertTrue(x.path == "code->devops")

		self.assertTrue(y.name == "Nature")
		self.assertTrue(y.path == "landscape->nature")

		x.save()
		y.save()

	def test_category_unicity(self): 
		'''two categories with same parents can t have the same name'''
		self.assertRaises(IntegrityError, Article_category.objects.create(parent=None, name="Code").save())
		self.assertRaises(IntegrityError, Photo_category.objects.create(parent=None, name="Landscape").save())

		with self.assertRaises(IntegrityError): 
			p = Article_category.objects.get(pk=1)
			Article_category.objects.create(parent=p, name="Python").save()

	def test_same_name_different_parents(self): 
		'''two categories with same names are possible IIF they dont have the same parent '''
		x = Article_category.objects.create(parent=None, name="News").save()
		y = Article_category.objects.create(parent=Article_category.objects.get(pk=1), name="News").save()

class TestArticleModel(TestCase): 
	fixtures = ["article_categories.yaml", "article-1.yaml", "person-1.yaml"]

	def test_unicity(self): 
		'''It sould be impossible for the same author to have two articles with the same name'''
		with self.assertRaises(IntegrityError):
			author = Person.objects.get(pk=1)
			Article.objects.create(title="Circa hos dies Lollianus primae lanuginis adulescens", 
			first_published= "2018-08-15",
			last_update = "2018-08-16",
			language="en",
			author=author,
			tags="a, duplicate", 
			content= "someting").save()

class TestPhotoModel(TestCase): 
	fixtures = ["photo_categories.yaml", "photo-1.yaml", "person-1.yaml"]

	def test_unicity(self): 
		'''It sould be impossible for the same author to have two pictures with the same title'''
		with self.assertRaises(IntegrityError):
			author = Person.objects.get(pk=1)
			Photo.objects.create(title="Hobbitebourg", 
			first_published= "2018-08-15",
			author=author,
			photo= "photo/img6.jpg").save()