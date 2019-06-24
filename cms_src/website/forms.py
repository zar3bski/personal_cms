from django import forms
from django.forms import ModelForm
from .models import Article_category, Photo, Message

class BrowseForm(forms.Form):
	class Meta: 
		model = Article_category

	def __init__(self, *args, **kwargs): 
		super(BrowseForm, self).__init__(*args, **kwargs)
		self.fields["super_category"]   = forms.ModelChoiceField(
			queryset=Article_category.objects.all(),
			label="", 
			widget= forms.Select(attrs={"class":"form-select"}),
			to_field_name="path")
		self.fields["order_mode"] = forms.ChoiceField(
			choices=[("last_update", "by last update"), ("rating", "by rate")],
			label="",
			widget=forms.RadioSelect())

class AddPictureForm(ModelForm):
	class Meta: 
		model   = Photo
		fields  = ["title","author","tags","family_friendly","description","photo_models","place_name","buy_link","photo"]
		labels  = {k:"" for k in fields}
	def __init__(self, *args, **kwargs): 
		super().__init__(*args, **kwargs)
		self.fields["title"].widget.attrs.update({'placeholder': 'Title', "class":"form-input"})
		self.fields["author"].widget.attrs.update({"class":"form-select"})
		self.fields["tags"].widget.attrs.update({'placeholder': 'Tags (, separated)', "class":"form-input"})
		self.fields["family_friendly"].widget.attrs.update({"class":"form-switch"})
		self.fields["description"].widget.attrs.update({'placeholder': 'Description', "class":"form-input"})
		self.fields["photo_models"].widget.attrs.update({"class":"form-select"})
		self.fields["place_name"].widget.attrs.update({'placeholder': 'Place Name', "class":"form-input"})
		self.fields["buy_link"].widget.attrs.update({'placeholder': 'Buy Link', "class":"form-input"})
		self.fields["photo"].widget.attrs.update({"class":"form-input"})

class MessageForm(ModelForm): 
	class Meta:
		model   = Message
		fields  = ["author", "mail", "subject", "content"]
		labels  = {k:"" for k in fields}
	def __init__(self, *args, **kwargs): 
		super().__init__(*args, **kwargs)
		self.fields["author"].widget.attrs.update({'placeholder': 'Your name', "class":"form-input"})
		self.fields["mail"].widget.attrs.update({'placeholder': 'Your email', "class":"form-input"})
		self.fields["subject"].widget.attrs.update({'placeholder': 'About', "class":"form-input"})
		self.fields["content"].widget.attrs.update({'placeholder': 'Message', "class":"form-input", "rows":"3"})

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
