from django import forms

from .models import Gallery


class AddGalleryForm(forms.ModelForm):

    class Meta:
        model = Gallery
        fields = ['title', 'description', 'is_published', 'is_public',]


class AddImagesForm(forms.Form):
    file_field = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
