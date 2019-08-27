from django.test import RequestFactory, TestCase, Client
from django.core.cache import cache
from django.db.utils import IntegrityError

from .models import Article_category, Photo_category, Article, Person, Photo, SiteSetting
from .views import Browse, Home, Project, Gallery

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
	'''NB: categories nedeed for caching'''
	fixtures = ["article_categories.yaml", "photo_categories.yaml", "person-1.yaml", "article-1.yaml"]

	def setUp(self):
		self.factory = RequestFactory()

	def test_access(self):
		c = Client()
		response = c.get("/browse/code->python/last_update/")
		self.assertEqual(response.status_code, 200)

	def test_data_retieval(self): 
		'''only articles under the browsed meta category and and children should be given'''
		request = self.factory.get('/browse/code/last_update')
		v = setup_view(Browse(), request)
		context = v._context_processor("code", "last_update", 1)

		self.assertTrue(len(context["articles"])==2)
		self.assertTrue(Article.objects.get(pk=1) in context["articles"])
		self.assertTrue(Article.objects.get(pk=2) in context["articles"])
		self.assertTrue(Article.objects.get(pk=3) not in context["articles"])	

# TODO
class TestHomeView(TestCase):
	pass

class TestGalleryView(TestCase):
	'''NB: categories nedeed for caching'''
	fixtures = ["photo_categories.yaml", "article_categories.yaml", "photo-1.yaml", "person-1.yaml"]

	def test_access(self):
		c = Client()
		response = c.get("/gallery/Landscape/")
		self.assertEqual(response.status_code, 200)

	def test_access_when_gallery_deactivated(self): 
		"""user should get a 404 when gallery is desactivated"""
		SiteSetting.objects.create(title= "My awsome site", owner_first_name= "John", url= "https://somewhere.overtherainbow.com", profil_image= "photo/Red_Panda_Simon_01.jpg", about= "Blog about photograpy, philosophy and code", keywords="code,python,django", display_bio= True, display_skills= True, display_carousel= True, show_gallery=False, show_articles= True, show_projects= True, show_education= True, show_jobs= True, show_certifications= True, owner_last_name= "Doe").save()
		c = Client()
		response = c.get("/gallery/Landscape/")
		self.assertEqual(response.status_code, 404)
		

class TestExperienceView(TestCase):
	'''NB: categories nedeed for caching'''
	fixtures = ["photo_categories.yaml", "article_categories.yaml", "job-1.yaml"]

	def test_access(self):
		c = Client()
		response = c.get("/timeline/Job/")
		self.assertEqual(response.status_code, 200)

class TestEducationView(TestCase):
	'''NB: categories nedeed for caching'''
	fixtures = ["photo_categories.yaml", "article_categories.yaml", "diplome-1.yaml"]

	def test_access(self):
		c = Client()
		response = c.get("/timeline/Diplome/")
		self.assertEqual(response.status_code, 200)

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

	def test_random_retrieval_by_category(self): 
		query = Article.get_random_instances(2, Article_category.objects.filter(path__startswith="code"))
		self.assertFalse(Article.objects.get(pk=3) in query)
		self.assertTrue(len(query)==2)
		self.assertIsInstance(query[0], Article)
		self.assertIsInstance(query[1], Article) 

	def test_random_retrieval_any(self): 
		query = Article.get_random_instances(1)
		self.assertIsInstance(query[0], Article) 

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

	def test_random_retrieval_by_category(self): 
		query = Photo.get_random_instances(1, Photo_category.objects.filter(path__startswith="landscape"))
		self.assertFalse(Photo.objects.get(pk=2) in query)
		self.assertIsInstance(query[0], Photo)

	def test_random_retrieval_any(self): 
		query = Photo.get_random_instances(1)
		self.assertIsInstance(query[0], Photo)

class TestPerson(TestCase): 
	fixtures = ["person-1.yaml"]

	def test_unicity_1(self):
		'''first name / last name combination are unique.'''
		with self.assertRaises(IntegrityError):
			Person.objects.create(first_name="Jack", last_name="the Ripper").save()
	
	def test_unicity_2(self):
		'''the same url cannot occur twice'''
		with self.assertRaises(IntegrityError):
			Person.objects.create(first_name="Mister", last_name="Nobody", url="https://fr.wikipedia.org/wiki/Jack_the_Ripper").save()
