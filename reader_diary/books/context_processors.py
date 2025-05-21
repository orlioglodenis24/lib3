from .models import Book, Genre, Author

def preview_data(request):
    return {
        'preview_books': Book.objects.all()[:3],
        'preview_genres': Genre.objects.all()[:3],
        'preview_authors': Author.objects.all()[:3],
    }
