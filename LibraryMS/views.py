from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Member
from django.contrib import messages
from django.views.generic import DetailView
from .models import Book, BookCopy
from .forms import AuthorUpdateForm, PublisherUpdateForm, AddBookForm


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
