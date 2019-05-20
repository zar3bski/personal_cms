'''from django import forms

class EducationForm(forms.Form):
	edu_type    = forms.ChoiceField(choices=[("diplom", "diplom"), ("certification", "certification")])
	title 		= forms.CharField(label='diploma / cert title', max_length=100)
	institution = forms.CharField(label='institution', max_length=100)
	link        = forms.URLField(label='institution link', required=False)
	year        = forms.IntegerField(label='year obtained')
	details     = forms.CharField(label='details', widget=forms.Textarea, required=False)'''
		