from django.shortcuts import render
from .models import BookInstance, Book, Author, Genre
import datetime


# Create your views here.
def index(request):
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='g').count()
    num_authors = Author.objects.all().count()
    my_context = {
        "num_books": num_books,
        "num_instances": num_instances,
        "num_instances_available": num_instances_available,
        "num_authors": num_authors,
        "now": datetime.datetime.today(),
    }
    return render(request, template_name='index.html', context=my_context)


def authors(request):
    authors = Author.objects.all()
    context = {
        'authors': authors,
    }
    return render(request, template_name="authors.html", context=context)
