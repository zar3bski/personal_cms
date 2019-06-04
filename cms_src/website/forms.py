from django import forms
from django.forms import ModelForm
from .models import Article_category, Photo

class BrowseForm(forms.Form):
	class Meta: 
		model = Article_category

	def __init__(self, init_cat=1, init_order="last_update", *args, **kwargs): 
		super(BrowseForm, self).__init__(*args, **kwargs)
		self.fields["category"]   = forms.ModelChoiceField(
			queryset=Article_category.objects.all(),
			initial=init_cat,
			label="")
		self.fields["order_mode"] = forms.ChoiceField(
			widget=forms.RadioSelect,
			choices=[("last_update", "by last update"), ("rating", "by rate")],
			initial=init_order,
			label="")

class AddPictureForm(ModelForm):
	class Meta: 
		model   = Photo
		fields  = ["title","author","tags","adult_only","description","photo_models","place_name","buy_link","photo"]
		labels = {k:"" for k in fields}
	def __init__(self, *args, **kwargs): 
		super().__init__(*args, **kwargs)
		self.fields["title"].widget.attrs.update({'placeholder': 'Title', "class":"form-input"})
		self.fields["author"].widget.attrs.update({"class":"form-select"})
		self.fields["tags"].widget.attrs.update({'placeholder': 'Tags (, separated)', "class":"form-input"})
		self.fields["adult_only"].widget.attrs.update({"class":"form-switch"})
		self.fields["description"].widget.attrs.update({'placeholder': 'Description', "class":"form-input"})
		self.fields["photo_models"].widget.attrs.update({"class":"form-select"})
		self.fields["place_name"].widget.attrs.update({'placeholder': 'Place Name', "class":"form-input"})
		self.fields["buy_link"].widget.attrs.update({'placeholder': 'Buy Link', "class":"form-input"})
		self.fields["photo"].widget.attrs.update({"class":"form-input"})

class CommentForm(forms.Form):
	author  = forms.CharField(
		label="", 
		max_length=100, 
		widget=forms.TextInput(attrs={'placeholder': 'Name', "class":"form-input"}))
	parent  = forms.IntegerField(
		label="",
		required=False, 
		widget=forms.HiddenInput(attrs={'placeholder': 'Answer to', "class":"form-input", "autocomplete":"off"}))
	content = forms.CharField(
		label="", 
		max_length=1000, 
		widget=forms.Textarea(attrs={"placeholder": "Your comment\n(you can use markdown syntax)","class":"form-input","row":"2"}))
