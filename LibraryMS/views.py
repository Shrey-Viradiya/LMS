from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from users.models import Member
from django.contrib import messages
from django.views.generic import DetailView
from .models import Book, BookCopy, BookHold, BookBorrowed
from .forms import AuthorUpdateForm, PublisherUpdateForm, AddBookForm, GiveBookForm, ReturnBookForm
from datetime import datetime, timedelta
from django.contrib.auth.models import User



# Create your views here.
@login_required
def dashboard(request):
    if Member.objects.filter(user=request.user).first() is None:
        messages.warning(request, 'You Need to first Update your profile.')
        return redirect('profile')
    else:
        return render(request, 'users/dashboard.html')


@login_required
def add_author(request):
    if Member.objects.filter(user=request.user).first() is None:
        messages.warning(request, 'You Need to first Update your profile.')
        return redirect('profile')
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = AuthorUpdateForm(request.POST)
            if form.is_valid():
                form.cleaned_data['name'] = form.cleaned_data['name'].title()
                form.save()
                author = form.cleaned_data.get('name')
                messages.success(request, f'Author entry created successfully for {author}!')
                return redirect('add-author')
        else:
            form = AuthorUpdateForm()
        return render(request, 'LibraryMS/AddAuthor.html', {'form': form})


@login_required
def add_book(request):
    if Member.objects.filter(user=request.user).first() is None:
        messages.warning(request, 'You Need to first Update your profile.')
        return redirect('profile')
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = AddBookForm(request.POST)
            if form.is_valid():
                ISBN = form.cleaned_data['ISBN']
                title = form.cleaned_data['title']
                price = form.cleaned_data['price']
                authors = form.cleaned_data['authors']
                publisher = form.cleaned_data['publishers']
                availability = form.cleaned_data['availability']

                avb = Book.objects.create(ISBN=ISBN, availability=availability, title=title, price=price,
                                          publisher=publisher)
                avb.save()

                for author in authors:
                    avb.authors.add(author)

                for _ in range(availability):
                    bk = BookCopy.objects.create(ISBN=avb)
                    bk.save()

                messages.success(request, f'Book entry created successfully for {title} !')
                return redirect('add-book')
        else:
            form = AddBookForm()

        return render(request, 'LibraryMS/AddBook.html', {'form': form})


@login_required
def add_publisher(request):
    if Member.objects.filter(user=request.user).first() is None:
        messages.warning(request, 'You Need to first Update your profile.')
        return redirect('profile')
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = PublisherUpdateForm(request.POST)
            if form.is_valid():
                form.save()
                name = form.cleaned_data.get('name')
                messages.success(request, f'Publisher entry created successfully for {name}!')
                return redirect('add-publisher')
        else:
            form = PublisherUpdateForm()
        return render(request, 'LibraryMS/AddPub.html', {'form': form})


class BookDetailView(DetailView):
    model = Book

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['copies'] = BookCopy.objects.filter(ISBN=self.get_object().ISBN)
        return context


@login_required
def HoldBook(request, pk):
    book = Book.objects.get(ISBN=pk)
    if book.availability > 0:
        messages.warning(request, 'You can not hold the book which are all ready available in the shelf!')
        return redirect('book-detail',pk = pk)
    else:
        book_copies = BookCopy.objects.filter(ISBN=book)

        reserved_book = BookHold.objects.all()
        reserved_book_id = []

        for _ in reserved_book:
            reserved_book_id.append(_.book.book_id)

        for bc in book_copies:
            if bc.book_id not in reserved_book_id:
                hld = BookHold.objects.create(book_id= bc.book_id, holder = request.user, res_date=datetime.now(), priority=abs(book.availability))
                hld.save()
                book.availability -= 1
                book.save()
                break
        messages.info(request, 'Book Reserved!')
        return redirect('book-detail', pk=pk)


@login_required
def GiveBook(request):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = GiveBookForm(request.POST)
            if form.is_valid():
                isbn = form.cleaned_data['ISBN']
                user = form.cleaned_data['user_id']

                book = get_object_or_404(Book, ISBN = isbn)
                usr = get_object_or_404(User,id=user)

                if book.availability <= 0:
                    check = BookHold.objects.filter(holder=usr)
                    for _ in check:
                        if _.book.ISBN == isbn:
                            bb = BookBorrowed.objects.create(borrower=usr, book=_, res_date=datetime.now(), due_date= datetime.now() + timedelta(days=14))
                            bb.save()
                            book.availability -= 1
                            book.save()
                            _.delete()
                            break
                    else:
                        messages.warning(request, 'Book Not Available!')
                        return redirect('give-book')
                else:
                    book_copies = BookCopy.objects.filter(ISBN=book)

                    reserved_book = BookHold.objects.all()
                    reserved_book_id = []

                    for _ in reserved_book:
                        reserved_book_id.append(_.book.book_id)

                    for bc in book_copies:
                        if bc.book_id not in reserved_book_id:
                            bb = BookBorrowed.objects.create(borrower=usr, book=bc, res_date=datetime.now(),
                                                             due_date=datetime.now() + timedelta(days=14))
                            bb.save()
                            book.availability -= 1
                            book.save()
                            break
                    messages.success(request, 'Book Given!')
                    return redirect('give-book')
        else:
            form = GiveBookForm()
        return render(request, 'LibraryMS/GiveBook.html', {'form': form})


@login_required
def ReturnBook(request):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = ReturnBookForm(request.POST)
            if form.is_valid():
                id = form.cleaned_data['book_id']

                bc = get_object_or_404(BookCopy, book_id = id)
                temp = get_object_or_404(BookBorrowed, book = bc)
                temp.delete()

                messages.success(request, 'Book Returned!')
                return redirect('return-book')

        else:
            form = ReturnBookForm()
        return render(request, 'LibraryMS/ReturnBook.html', {'form': form})


def home(request):
    if request.method == 'GET':
        query= request.GET.get('q')

        submitbutton = request.GET.get('submit')

        if query is not None:
            query = query.title()
            lookups= Q(title__icontains=query) | Q(authors__name__icontains=query) | Q(publisher__name__icontains=query)

            results= Book.objects.filter(lookups).distinct()

            context={'results': results,
                     'submitbutton': submitbutton}
            return render(request, 'LibraryMS/home.html', context)

        else:
            return render(request, 'LibraryMS/home.html')

    else:
        return render(request, 'LibraryMS/home.html')
