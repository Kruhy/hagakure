from django import forms


class ArticlePublicationStatusForm(forms.Form):
    is_published = forms.TypedMultipleChoiceField(required=False)
    is_public = forms.TypedMultipleChoiceField(required=False)
