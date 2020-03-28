from django.core.mail import send_mass_mail
from background_task import background
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from LibraryMS.models import BookHold, BookBorrowed

@background()
def SendEmails():
    today = datetime.today().date()

    admin = User.objects.get(pk=1)
    admin.email_user('Testing Background Function',f'Start of the function {datetime.now()}')

    last_msg = f'End of the function {datetime.now()}\n'

    # hlds = BookHold.objects.filter(available=3)
    # # last_msg+=str(hlds)
    # msgs = (('Advanced Book Due Notice',
    #          f'Dear {_.holder.first_name} {_.holder.last_name},\nYour book {_.book.title} is not picked up by you. Your hold is released',
    #          'LibraryManagementSystem', [_.holder.email]) for _ in hlds)
    # send_mass_mail(msgs, fail_silently=True)
    # 
    # for _ in hlds:
    #     _.book.availability+=1
    #     _.book.save()
    #     _.delete()
    # 
    # hlds = BookHold.objects.filter(available=1)
    # # last_msg += str(hlds)
    # for _ in hlds:
    #     _.available+=1
    #     _.save()
    # 
    # hlds = BookHold.objects.filter(available=2)
    # # last_msg += str(hlds)
    # for _ in hlds:
    #     _.available += 1
    #     _.save()
    # 
    # brd = BookBorrowed.objects.filter(due_date__day=today - timedelta(days=2))
    # # last_msg += str(brd)
    # msgs = (('Advanced Book Due Notice',f'Dear {book.borrower.first_name} {book.borrower.last_name},\nYour book {book.book.ISBN.title} will be due in 2 days','LibraryManagementSystem',[book.borrower.email]) for book in brd)
    # send_mass_mail(msgs,fail_silently=True)
    # 
    # brd = BookBorrowed.objects.filter(due_date__day=today)
    # # last_msg += str(brd)
    # msgs = (('Book Due Notice',
    #              f'Dear {book.borrower.first_name} {book.borrower.last_name},\nYour book {book.book.ISBN.title} is due today. Please Return ASAP.',
    #              'LibraryManagementSystem', [book.borrower.email]) for book in brd)
    # send_mass_mail(msgs, fail_silently=True)

    admin.email_user('Testing Background Function', last_msg)