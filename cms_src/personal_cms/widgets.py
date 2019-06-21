from django import forms
from django.conf import settings

class CssEditor(forms.Textarea):
    def __init__(self, *args, **kwargs):
        super(CssEditor, self).__init__(*args, **kwargs)
        self.attrs['class'] = 'html-editor'

    class Media:
        css = {
            'all': (
                'https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.47.0/codemirror.css',
            )
        }
        js = (
            settings.STATIC_URL+'/website/script/codemirror.js',
            settings.STATIC_URL+'/website/script/css.js',
            settings.STATIC_URL+'/website/script/codemirror-init.js'
        )