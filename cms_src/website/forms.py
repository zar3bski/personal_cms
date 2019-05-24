from django import forms
from .models import Category

class BrowseForm(forms.Form):
	class Meta: 
		model = Category

	def __init__(self, init_cat=1, init_order="last_update", *args, **kwargs): 
		super(BrowseForm, self).__init__(*args, **kwargs)
		self.fields["category"]   = forms.ModelChoiceField(
			queryset=Category.objects.all(),
			initial=init_cat,
			label="")
		self.fields["order_mode"] = forms.ChoiceField(
			widget=forms.RadioSelect,
			choices=[("last_update", "by last update"), ("rating", "by rate")],
			initial=init_order,
			label="")
		