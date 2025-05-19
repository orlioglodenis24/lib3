from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Book, Author, Genre, BookReview, ReadingStatus
from .forms import BookReviewForm, ReadingStatusForm, BookSearchForm

# books/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # после регистрации идём на логин
    else:
        form = UserCreationForm()
    return render(request, 'books/register.html', {'form': form})


def index(request):
    """Homepage view showing latest books and popular titles."""
    latest_books = Book.objects.all().order_by('-created')[:12]
    popular_books = Book.objects.annotate(
        avg_rating=Avg('reviews__rating'),
        num_reviews=Count('reviews')
    ).order_by('-avg_rating', '-num_reviews')[:12]
    
    trending_books = Book.objects.annotate(
        reading_count=Count('reading_statuses', 
                        filter=Q(reading_statuses__status='reading'))
    ).order_by('-reading_count')[:12]
    
    genres = Genre.objects.all()[:10]
    
    return render(request, 'books/index.html', {
        'latest_books': latest_books,
        'popular_books': popular_books,
        'trending_books': trending_books,
        'genres': genres,
    })
from django.contrib.auth.views import LogoutView

class LogoutGetAllowedView(LogoutView):
    # Разрешить logout по GET
    http_method_names = ['get', 'post']
    
def book_list(request):
    """View for listing all books with search and filter functionality."""
    form = BookSearchForm(request.GET)
    books = Book.objects.all()
    
    if form.is_valid():
        query = form.cleaned_data.get('query')
        genre = form.cleaned_data.get('genre')
        status = form.cleaned_data.get('status')
        sort = form.cleaned_data.get('sort', '-created')
        
        if query:
            books = books.filter(
                Q(title__icontains=query) | 
                Q(description__icontains=query) |
                Q(authors__name__icontains=query)
            ).distinct()
        
        if genre:
            books = books.filter(genres__slug=genre)
        
        if status:
            books = books.filter(status=status)
        
        books = books.order_by(sort)
    
    # Pagination
    paginator = Paginator(books, 24)  # 24 books per page
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    return render(request, 'books/book_list.html', {
        'books': books,
        'form': form,
        'genres': Genre.objects.all(),
    })


def book_detail(request, slug):
    """View for book details and user interaction."""
    book = get_object_or_404(Book, slug=slug)
    reviews = book.reviews.all()
    
    # Get similar books based on genres
    similar_books = Book.objects.filter(genres__in=book.genres.all()).exclude(id=book.id).distinct()[:6]
    
    # Check if the user has a reading status for this book
    user_status = None
    if request.user.is_authenticated:
        try:
            user_status = ReadingStatus.objects.get(user=request.user, book=book)
        except ReadingStatus.DoesNotExist:
            pass
    
    # Review form handling
    if request.method == 'POST' and request.user.is_authenticated:
        review_form = BookReviewForm(request.POST)
        if review_form.is_valid():
            review = review_form.save(commit=False)
            review.book = book
            review.user = request.user
            
            # Check if user already reviewed this book
            try:
                existing_review = BookReview.objects.get(user=request.user, book=book)
                existing_review.rating = review.rating
                existing_review.comment = review.comment
                existing_review.save()
                messages.success(request, "Your review has been updated.")
            except BookReview.DoesNotExist:
                review.save()
                messages.success(request, "Your review has been added.")
                
            return redirect('book_detail', slug=slug)
    else:
        # If user already has a review, populate the form with it
        if request.user.is_authenticated:
            try:
                user_review = BookReview.objects.get(user=request.user, book=book)
                review_form = BookReviewForm(instance=user_review)
            except BookReview.DoesNotExist:
                review_form = BookReviewForm()
        else:
            review_form = BookReviewForm()
    
    # Reading status form
    status_form = ReadingStatusForm(instance=user_status)
            
    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'similar_books': similar_books,
        'review_form': review_form,
        'status_form': status_form,
        'user_status': user_status,
    })


def author_detail(request, slug):
    """View for author details and their books."""
    author = get_object_or_404(Author, slug=slug)
    books = author.books.all()
    
    return render(request, 'books/author_detail.html', {
        'author': author,
        'books': books,
    })


def genre_detail(request, slug):
    """View for genre details and books in this genre."""
    genre = get_object_or_404(Genre, slug=slug)
    books = genre.books.all()
    
    # Pagination
    paginator = Paginator(books, 24)
    page = request.GET.get('page')
    
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    
    return render(request, 'books/genre_detail.html', {
        'genre': genre,
        'books': books,
    })


@login_required
@require_POST
def update_reading_status(request, book_id):
    """View for updating user's reading status for a book."""
    book = get_object_or_404(Book, id=book_id)
    
    try:
        status = ReadingStatus.objects.get(user=request.user, book=book)
    except ReadingStatus.DoesNotExist:
        status = ReadingStatus(user=request.user, book=book)
    
    form = ReadingStatusForm(request.POST, instance=status)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Reading status updated successfully!")
        return redirect('book_detail', slug=book.slug)
    
    messages.error(request, "There was an error updating your reading status.")
    return redirect('book_detail', slug=book.slug)


@login_required
def my_library(request):
    """View for user's reading list/library."""
    reading = ReadingStatus.objects.filter(
        user=request.user, status='reading'
    ).select_related('book')
    
    completed = ReadingStatus.objects.filter(
        user=request.user, status='completed'
    ).select_related('book')
    
    plan_to_read = ReadingStatus.objects.filter(
        user=request.user, status='plan_to_read'
    ).select_related('book')
    
    dropped = ReadingStatus.objects.filter(
        user=request.user, status='dropped'
    ).select_related('book')
    
    return render(request, 'books/my_library.html', {
        'reading': reading,
        'completed': completed,
        'plan_to_read': plan_to_read,
        'dropped': dropped,
    })


@login_required
@require_POST
def update_progress(request, status_id):
    """AJAX view for updating reading progress."""
    status = get_object_or_404(ReadingStatus, id=status_id, user=request.user)
    
    try:
        progress = int(request.POST.get('progress', 0))
        status.progress = progress
        status.save()
        return JsonResponse({'success': True, 'progress': progress})
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid progress value'}, status=400)