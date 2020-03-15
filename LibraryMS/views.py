from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from users.models import Member
from django.contrib import messages
from .models import Book, Author, Publisher
from .forms import AuthorUpdateForm, PublisherUpdateForm, BookUpdateForm


# Create your views here.
@login_required
def dashboard(request):
    if Member.objects.filter(user=request.user).first() is None:
        return redirect('profile')
    else:
        return render(request, 'users/dashboard.html')


@login_required
def add_author(request):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = AuthorUpdateForm(request.POST)
            if form.is_valid():
                form.save()
                author = form.cleaned_data.get('name')
                messages.success(request, f'Author entry created successfully for {author}!')
                return redirect('add-author')
        else:
            form = AuthorUpdateForm()
        return render(request, 'LibraryMS/AddAuthor.html', {'form': form})


@login_required
def add_book(request):
    if not request.user.is_staff:
        messages.warning(request, 'You are not authorised to requested page.')
        return redirect('Member-dashboard')
    else:
        if request.method == 'POST':
            form = BookUpdateForm(request.POST)
            if form.is_valid():
                form.save()
                title = form.cleaned_data.get('title')
                messages.success(request, f'Book entry created successfully for {title}!')
                return redirect('add-book')
        else:
            form = BookUpdateForm()
        return render(request, 'LibraryMS/AddBook.html', {'form': form})


@login_required
def add_publisher(request):
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
