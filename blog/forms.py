from django import forms
from .models import Article, ArticleImage

ALLOWED_CONTENT_TYPES = ['image/jpeg', 'image/png', 'image/gif', 'image/bmp', 'image/webp']


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        labels = {
            'title': 'Заголовок',
            'content': 'Текст статті',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['content'].widget.attrs.update({'class': 'form-control', 'rows': '10'})

class ArticleImageForm(forms.ModelForm):
    class Meta:
        model = ArticleImage
        fields = ['image']

    def clean_image(self):
        image = self.cleaned_data.get('image')

        if image:
            if image.content_type not in ALLOWED_CONTENT_TYPES:
                raise forms.ValidationError('Дозволено лише зображення: jpeg, png, gif, bmp, webp.')
        return image