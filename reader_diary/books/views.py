from rest_framework import viewsets
from .serializers import GenreSerializer, BookSerializer, UserBookStatusSerializer, DiaryEntrySerializer, QuoteSerializer
from .models import Genre, Book, UserBookStatus, ReadingDiaryEntry, Quote

from django.shortcuts import render
from .models import Book
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Book
from .models import Genre, Author,Book

class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class UserBookStatusViewSet(viewsets.ModelViewSet):
    queryset = UserBookStatus.objects.all()
    serializer_class = UserBookStatusSerializer

class DiaryEntryViewSet(viewsets.ModelViewSet):
    queryset = ReadingDiaryEntry.objects.all()
    serializer_class = DiaryEntrySerializer

class QuoteViewSet(viewsets.ModelViewSet):
    queryset = Quote.objects.all()
    serializer_class = QuoteSerializer


def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def index(request):
    return render(request, 'index.html')

def profile(request):
    context = {
        # данные для шаблона
    }
    return render(request, 'profile.html', context)

def user_books(request):
    return render(request, 'user_books.html')

def catalog(request):
    books = Book.objects.all()
    return render(request, 'catalog.html', {'books': books})

def genres(request):
    genres_list = Genre.objects.all()
    return render(request, 'genres.html', {'genres': genres_list})

# def authors(request):
#     authors_list = Author.objects.all()  
#     context = {
#         'authors': authors_list, 
#     }
#     return render(request, 'authors.html', context)

def diary(request):
    # логика для страницы дневника
    return render(request, 'diary.html')

def profile_edit(request):
    if request.method == 'POST':
        # обработка формы, сохранение изменений
        ...
        return redirect('profile')  # после успешного сохранения редирект на профиль
    else:
        # отобразить форму редактирования
        return render(request, 'profile_edit.html')
    

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book_detail.html', {'book': book})

# def genres(request):
#     genres = Genre.objects.all()
#     return render(request, 'genres.html', {'genres': genres})

# def authors(request):
#     authors = Author.objects.all()
#     return render(request, 'authors.html', {'authors': authors})

def genres_and_authors(request):
    authors = Author.objects.all()
    genres = Genre.objects.all()
    context = {
        'authors': authors,
        'genres': genres,
    }
    return render(request, 'genres_and_authors.html', context)


def catalog(request):
    books = Book.objects.all()
    genres = Genre.objects.all()
    authors = Author.objects.all()

    q = request.GET.get('q', '')
    genre_id = request.GET.get('genre', '')
    author_id = request.GET.get('author', '')
    year = request.GET.get('year', '')

    if q:
        books = books.filter(title__icontains=q) | books.filter(author__name__icontains=q)

    if genre_id:
        books = books.filter(genre_id=genre_id)

    if author_id:
        books = books.filter(author_id=author_id)

    if year:
        books = books.filter(publication_year=year)  # Убедись, что в модели есть поле publication_year

    context = {
        'books': books,
        'genres': genres,
        'authors': authors,
    }
    return render(request, 'catalog.html', context)

def catalog_view(request):
    books_list = Book.objects.all().order_by('title')
    paginator = Paginator(books_list, 12)  
    page_number = request.GET.get('page') or 1
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'catalog.html', context)