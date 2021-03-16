from django import forms

from .models import Article


class ArticlePublicationStatusForm(forms.Form):
    is_published = forms.TypedMultipleChoiceField(required=False)
    is_public = forms.TypedMultipleChoiceField(required=False)


class AddArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title','synopsis', 'body', 'category', 'is_published', 'is_public',)
