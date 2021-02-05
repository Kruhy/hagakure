from django import forms

from .models import News


class NewsPublicationStatusForm(forms.Form):
    is_published = forms.TypedMultipleChoiceField(required=False)
    is_public = forms.TypedMultipleChoiceField(required=False)


class AddNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = ('title','body', 'is_published', 'is_public', 'expiration_date',)
