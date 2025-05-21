from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.utils.text import slugify
from django.urls import reverse

from .models import Book, Author, Genre, BookReview, ReadingStatus, BookDiaryEntry, BookQuote, Publisher
from .forms import (
    BookReviewForm, ReadingStatusForm, BookSearchForm, BookDiaryEntryForm, 
    BookQuoteForm, BookUploadForm
)
from .auth_views import register  # Импортируем функцию регистрации


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
            books = books.filter(genres=genre)
        
        if status:
            books = books.filter(status=status)
        
        books = books.order_by(sort)
    
    # Include average ratings for book display
    books = books.annotate(avg_rating=Avg('reviews__rating'))
    
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
    quotes = book.quotes.all()[:5]  # Get up to 5 quotes
    
    # Get similar books based on genres
    similar_books = Book.objects.filter(genres__in=book.genres.all()).exclude(id=book.id).distinct()[:6]
    
    # Check if the user has a reading status for this book
    user_status = None
    user_diary_entry = None
    user_review = None
    
    if request.user.is_authenticated:
        try:
            user_status = ReadingStatus.objects.get(user=request.user, book=book)
        except ReadingStatus.DoesNotExist:
            pass
            
        try:
            user_diary_entry = BookDiaryEntry.objects.get(user=request.user, book=book)
        except BookDiaryEntry.DoesNotExist:
            pass
            
        try:
            user_review = BookReview.objects.get(user=request.user, book=book)
        except BookReview.DoesNotExist:
            pass
    
    # Forms
    review_form = BookReviewForm(instance=user_review) if user_review else BookReviewForm()
    status_form = ReadingStatusForm(instance=user_status) if user_status else ReadingStatusForm()
    diary_form = BookDiaryEntryForm(instance=user_diary_entry) if user_diary_entry else BookDiaryEntryForm()
    quote_form = BookQuoteForm()
            
    return render(request, 'books/book_detail.html', {
        'book': book,
        'reviews': reviews,
        'quotes': quotes,
        'similar_books': similar_books,
        'review_form': review_form,
        'status_form': status_form,
        'diary_form': diary_form,
        'quote_form': quote_form,
        'user_status': user_status,
        'user_diary_entry': user_diary_entry,
    })


def author_detail(request, slug):
    """View for author details and their books."""
    author = get_object_or_404(Author, slug=slug)
    books = author.books.all().annotate(avg_rating=Avg('reviews__rating'))
    
    return render(request, 'books/author_detail.html', {
        'author': author,
        'books': books,
    })


def genre_detail(request, slug):
    """View for genre details and books in this genre."""
    genre = get_object_or_404(Genre, slug=slug)
    books = genre.books.all().annotate(avg_rating=Avg('reviews__rating'))
    
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
        status = form.save(commit=False)
        
        # If status is changed to 'completed', set end_date to today if not provided
        if status.status == 'completed' and not status.end_date:
            status.end_date = timezone.now().date()
            
        # If status is changed to 'reading', set start_date to today if not provided
        if status.status == 'reading' and not status.start_date:
            status.start_date = timezone.now().date()
            
        status.save()
        messages.success(request, "Reading status updated successfully!")
    else:
        messages.error(request, "There was an error updating your reading status.")
    
    return redirect('book_detail', slug=book.slug)


@login_required
@require_POST
def update_progress(request, status_id):
    """AJAX view for updating reading progress."""
    status = get_object_or_404(ReadingStatus, id=status_id, user=request.user)
    
    try:
        progress = int(request.POST.get('progress', 0))
        status.progress = progress
        status.last_read_date = timezone.now().date()
        status.save()
        
        # If progress is equal to book's page count and book has pages, mark as completed
        if status.book.page_count and progress >= status.book.page_count:
            status.status = 'completed'
            if not status.end_date:
                status.end_date = timezone.now().date()
            status.save()
            
        return JsonResponse({
            'success': True, 
            'progress': progress,
            'status': status.status,
        })
    except (ValueError, TypeError):
        return JsonResponse({'success': False, 'error': 'Invalid progress value'}, status=400)


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
    
    # Add some statistics
    total_books = reading.count() + completed.count() + plan_to_read.count() + dropped.count()
    total_pages_read = sum(s.progress for s in completed) + sum(s.progress for s in reading)
    
    # Get user's reviews
    reviews = BookReview.objects.filter(user=request.user).select_related('book')
    
    return render(request, 'books/my_library.html', {
        'reading': reading,
        'completed': completed,
        'plan_to_read': plan_to_read,
        'dropped': dropped,
        'reviews': reviews,
        'total_books': total_books,
        'total_pages_read': total_pages_read,
    })


@login_required
@require_POST
def add_book_review(request, book_id):
    """View for adding/updating book reviews."""
    book = get_object_or_404(Book, id=book_id)
    
    try:
        review = BookReview.objects.get(user=request.user, book=book)
    except BookReview.DoesNotExist:
        review = BookReview(user=request.user, book=book)
    
    form = BookReviewForm(request.POST, instance=review)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Your review has been saved.")
    else:
        messages.error(request, "There was an error saving your review.")
    
    return redirect('book_detail', slug=book.slug)


@login_required
@require_POST
def add_diary_entry(request, book_id):
    """View for adding/updating book diary entries."""
    book = get_object_or_404(Book, id=book_id)
    
    try:
        entry = BookDiaryEntry.objects.get(user=request.user, book=book)
    except BookDiaryEntry.DoesNotExist:
        entry = BookDiaryEntry(user=request.user, book=book)
    
    form = BookDiaryEntryForm(request.POST, instance=entry)
    
    if form.is_valid():
        form.save()
        messages.success(request, "Your diary entry has been saved.")
    else:
        messages.error(request, "There was an error saving your diary entry.")
    
    return redirect('book_detail', slug=book.slug)


@login_required
@require_POST
def add_book_quote(request, book_id):
    """View for adding book quotes."""
    book = get_object_or_404(Book, id=book_id)
    form = BookQuoteForm(request.POST)
    
    if form.is_valid():
        quote = form.save(commit=False)
        quote.user = request.user
        quote.book = book
        quote.save()
        messages.success(request, "Quote added successfully.")
    else:
        messages.error(request, "There was an error adding your quote.")
    
    return redirect('book_detail', slug=book.slug)


@login_required
def delete_book_quote(request, quote_id):
    """View for deleting book quotes."""
    quote = get_object_or_404(BookQuote, id=quote_id, user=request.user)
    book_slug = quote.book.slug
    quote.delete()
    messages.success(request, "Quote deleted successfully.")
    
    return redirect('book_detail', slug=book_slug)


@login_required
def add_book(request):
    """View for users to add new books."""
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.slug = slugify(book.title)
            book.added_by = request.user
            
            # Handle new author if provided
            new_author_name = form.cleaned_data.get('new_author')
            if new_author_name and not form.cleaned_data.get('authors'):
                author, created = Author.objects.get_or_create(
                    name=new_author_name,
                    defaults={'slug': slugify(new_author_name)}
                )
                book.save()
                book.authors.add(author)
            else:
                book.save()
                if form.cleaned_data.get('authors'):
                    book.authors.set(form.cleaned_data.get('authors'))
            
            # Handle new publisher if provided
            new_publisher_name = form.cleaned_data.get('new_publisher')
            if new_publisher_name and not form.cleaned_data.get('publisher'):
                publisher, created = Publisher.objects.get_or_create(
                    name=new_publisher_name,
                    defaults={'slug': slugify(new_publisher_name)}
                )
                book.publisher = publisher
                book.save()
            
            # Add genres
            book.genres.set(form.cleaned_data.get('genres'))
            
            messages.success(request, f"Book '{book.title}' added successfully!")
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookUploadForm()
    
    return render(request, 'books/add_book.html', {
        'form': form,
    })


@login_required
def edit_book(request, book_id):
    """View for editing books (only for book creators or staff)."""
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user is the creator or staff
    if book.added_by != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to edit this book.")
        return redirect('book_detail', slug=book.slug)
    
    if request.method == 'POST':
        form = BookUploadForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            messages.success(request, f"Book '{book.title}' updated successfully!")
            return redirect('book_detail', slug=book.slug)
    else:
        form = BookUploadForm(instance=book)
    
    return render(request, 'books/edit_book.html', {
        'form': form,
        'book': book,
    })


@login_required
def delete_book(request, book_id):
    """View for deleting books (only for book creators or staff)."""
    book = get_object_or_404(Book, id=book_id)
    
    # Check if user is the creator or staff
    if book.added_by != request.user and not request.user.is_staff:
        messages.error(request, "You don't have permission to delete this book.")
        return redirect('book_detail', slug=book.slug)
    
    if request.method == 'POST':
        title = book.title
        book.delete()
        messages.success(request, f"Book '{title}' deleted successfully!")
        return redirect('book_list')
    
    return render(request, 'books/delete_book.html', {
        'book': book,
    })


@login_required
def user_profile(request):
    """View for user profile page with statistics."""
    # Reading statistics
    reading_statuses = ReadingStatus.objects.filter(user=request.user)
    total_books_read = reading_statuses.filter(status='completed').count()
    currently_reading = reading_statuses.filter(status='reading').count()
    plan_to_read = reading_statuses.filter(status='plan_to_read').count()
    
    # Pages statistics
    total_pages_read = sum(
        s.progress for s in reading_statuses.filter(status='completed')
    ) + sum(
        s.progress for s in reading_statuses.filter(status='reading')
    )
    
    # Review statistics
    reviews = BookReview.objects.filter(user=request.user)
    avg_rating = reviews.aggregate(Avg('rating'))['rating__avg'] or 0
    
    # Favorite genres based on read books
    read_books = Book.objects.filter(
        reading_statuses__user=request.user,
        reading_statuses__status__in=['completed', 'reading']
    )
    genre_counts = Genre.objects.filter(books__in=read_books).annotate(
        count=Count('id')
    ).order_by('-count')[:5]
    
    # Recent activity
    recent_statuses = reading_statuses.order_by('-last_read_date')[:5]
    recent_reviews = reviews.order_by('-created')[:5]
    
    return render(request, 'books/user_profile.html', {
        'total_books_read': total_books_read,
        'currently_reading': currently_reading,
        'plan_to_read': plan_to_read,
        'total_pages_read': total_pages_read,
        'avg_rating': avg_rating,
        'genre_counts': genre_counts,
        'recent_statuses': recent_statuses,
        'recent_reviews': recent_reviews,
    })