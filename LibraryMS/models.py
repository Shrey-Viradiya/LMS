from django.db import models
from django.contrib.auth.models import User

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
    ISBN = models.CharField(max_length=13, primary_key=True)
    availability = models.IntegerField()
    title = models.CharField(max_length=255, default="NA")
    price = models.PositiveIntegerField(default=0)
    authors = models.ManyToManyField(Author)
    publisher = models.ForeignKey(Publisher, on_delete=SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"Book ID {self.ISBN}: {self.title}"


class BookCopy(models.Model):
    book_id = models.AutoField(primary_key=True)
    ISBN = models.ForeignKey(Book, on_delete=models.CASCADE)

    def __str__(self):
        return f"Book ID {self.book_id}: {self.ISBN.title}"


class BookHold(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    holder = models.ForeignKey(User, on_delete=models.CASCADE)
    res_date = models.DateTimeField()
    priority = models.PositiveIntegerField()

    def __str__(self):
        return f"Book {self.book.ISBN} held By User ID {self.holder.id}"


class BookBorrowed(models.Model):
    book = models.OneToOneField(BookCopy, on_delete=models.CASCADE)
    borrower = models.ForeignKey(User, on_delete=models.CASCADE)
    res_date = models.DateTimeField()
    due_date = models.DateTimeField()

    def __str__(self):
        return f"Book {self.book.book_id} Borrowed By User ID {self.borrower.id}"