from django.shortcuts import render
from django.http import HttpResponse
from . import models
from django.views.generic import CreateView, DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here.


def index(request):
    num_books = models.Book.objects.all().count()
    num_instances = models.BookInstance.objects.all().count()
    num_instances_avail = models.BookInstance.objects.filter(status__exact='a').count()

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_avail': num_instances_avail
    }

    return render(request, 'catalog/index.html', context=context)

class ListAllBooks(ListView, LoginRequiredMixin):
    model = models.Book
    fields="__all__"
    template_name = "book_list.html"


class BookCreate(LoginRequiredMixin, CreateView):
    model = models.Book
    fields = '__all__'

class BookDetail(DetailView):
    model = models.Book

@login_required
def my_view(request):
    return render(request, 'catalog/my_view.html')

class CheckedOutBooksByUserView(LoginRequiredMixin, ListView):
    model = models.BookInstance
    template_name = 'catalog/profile.html'
    paginate_by = 10

    def get_queryset(self):
        return models.BookInstance.objects.filter(borrower=self.request.user).all()