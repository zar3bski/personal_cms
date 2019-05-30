from django import forms
from .models import Article_category

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
