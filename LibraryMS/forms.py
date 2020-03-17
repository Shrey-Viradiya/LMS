from django import forms
from .models import Book, Author, Publisher, Availability


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class PublisherUpdateForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address']


class AddBookForm(forms.Form):
    ISBN = forms.IntegerField(label='ISBN', min_value=0, max_value=9999999999999)
    title = forms.CharField(label='Title', max_length=255)
    price = forms.IntegerField(label = 'Price', min_value=0)
    authors = forms.ModelMultipleChoiceField(label='Authors', queryset=Author.objects.all())
    publishers = forms.ModelChoiceField(label='Publishers', queryset=Publisher.objects.all())
    availability = forms.IntegerField(label = 'Availability', min_value=0)


