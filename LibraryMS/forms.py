from django import forms
from .models import Book, Author, Publisher


class AuthorUpdateForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name']


class PublisherUpdateForm(forms.ModelForm):
    class Meta:
        model = Publisher
        fields = ['name', 'address']


class BookUpdateForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['ISBN', 'title', 'price', 'availability', 'authors', 'publisher']

