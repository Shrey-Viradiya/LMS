from django.db import models


# Create your models here.
from django.db.models import SET_NULL


class Author(models.Model):
    author_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name


class Publisher(models.Model):
    pub_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=256)
    address = models.TextField(null=False)

    def __str__(self):
        return self.name


class Book(models.Model):
    book_id = models.AutoField(primary_key=True)
    ISBN = models.BigIntegerField(max_length=13)
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    availability = models.IntegerField()
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=SET_NULL, blank=True, null= True)

    def __str__(self):
        return f"{self.title} with ISBN {self.ISBN}"
