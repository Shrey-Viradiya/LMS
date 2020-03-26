from django.contrib import admin
from .models import Author, Book, Publisher, BookCopy, BookHold, BookBorrowed


# Register your models here.
admin.site.register(Author)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(BookCopy)
admin.site.register(BookHold)
admin.site.register(BookBorrowed)
