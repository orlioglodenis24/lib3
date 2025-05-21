# from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required
# from django.views.decorators.http import require_POST
# from django.shortcuts import get_object_or_404
# from django.utils import timezone
# from django.template.loader import render_to_string
# from django.core.paginator import Paginator

# from .models import Book, Genre, Author, BookReview, ReadingStatus, BookQuote
# from .forms import BookQuoteForm

# @require_POST
# @login_required
# def toggle_reading_status(request):
#     """AJAX view to quickly toggle reading status."""
#     book_id = request.POST.get('book_id')
#     new_status = request.POST.get('status')
    
#     if not book_id or not new_status:
#         return JsonResponse({'success': False, 'error': 'Invalid parameters'}, status=400)
        
#     book = get_object_or_404(Book, id=book_id)
    
#     try:
#         status = ReadingStatus.objects.get(user=request.user, book=book)
#         if status.status == new_status:
#             # If already in this status, remove it
#             status.delete()
#             return JsonResponse({'success': True, 'action': 'removed', 'status': new_status})
#         else:
#             # Update to new status
#             status.status = new_status
            
#             # Set appropriate dates
#             if new_status == 'reading' and not status.start_date:
#                 status.start_date = timezone.now().date()
#             elif new_status == 'completed' and not status.end_date:
#                 status.end_date = timezone.now().date()
                
#             status.save()
#             return JsonResponse({'success': True, 'action': 'updated', 'status': new_status})
#     except ReadingStatus.DoesNotExist:
#         # Create new status
#         status = ReadingStatus(
#             user=request.user,
#             book=book,
#             status=new_status,
#         )
        
#         # Set appropriate dates
#         if new_status == 'reading':
#             status.start_date = timezone.now().date()
#         elif new_status == 'completed':
#             status.end_date = timezone.now().date()
            
#         status.save()
#         return JsonResponse({'success': True, 'action': 'added', 'status': new_status})


# @require_POST
# @login_required
# def quick_rate(request):
#     """AJAX view to quickly rate a book."""
#     book_id = request.POST.get('book_id')
#     rating = request.POST.get('rating')
    
#     if not book_id or not rating:
#         return JsonResponse({'success': False, 'error': 'Invalid parameters'}, status=400)
        
#     try:
#         rating = int(rating)
#         if rating < 1 or rating > 10:
#             raise ValueError("Rating must be between 1 and 10")
#     except ValueError:
#         return JsonResponse({'success': False, 'error': 'Invalid rating value'}, status=400)
    
#     book = get_object_or_404(Book, id=book_id)
    
#     try:
#         review = BookReview.objects.get(user=request.user, book=book)
#         review.rating = rating
#         review.save()
#     except BookReview.DoesNotExist:
#         review = BookReview(
#             user=request.user,
#             book=book,
#             rating=rating
#         )
#         review.save()
    
#     # Calculate new average rating
#     avg_rating = book.get_average_rating()
    
#     return JsonResponse({
#         'success': True, 
#         'rating': rating,
#         'avg_rating': avg_rating
#     })


# @login_required
# def load_more_quotes(request):
#     """AJAX view to load more quotes for a book."""
#     book_id = request.GET.get('book_id')
#     page = request.GET.get('page', 1)
    
#     if not book_id:
#         return JsonResponse({'success': False, 'error': 'Book ID is required'}, status=400)
    
#     book = get_object_or_404(Book, id=book_id)
#     quotes = book.quotes.all().order_by('-created')
    
#     paginator = Paginator(quotes, 5)  # 5 quotes per page
    
#     try:
#         quotes_page = paginator.page(page)
#     except:
#         return JsonResponse({'success': False, 'error': 'Invalid page'}, status=400)
    
#     quotes_html = render_to_string(
#         'books/partials/quotes_list.html',
#         {'quotes': quotes_page, 'book': book, 'user': request.user}
#     )
    
#     return JsonResponse({
#         'success': True,
#         'quotes_html': quotes_html,
#         'has_next': quotes_page.has_next(),
#         'next_page': quotes_page.next_page_number() if quotes_page.has_next() else None
#     })


# @require_POST
# @login_required
# def ajax_add_quote(request):
#     """AJAX view to add a book quote."""
#     book_id = request.POST.get('book_id')
    
#     if not book_id:
#         return JsonResponse({'success': False, 'error': 'Book ID is required'}, status=400)
        
#     book = get_object_or_404(Book, id=book_id)
#     form = BookQuoteForm(request.POST)
    
#     if form.is_valid():
#         quote = form.save(commit=False)
#         quote.user = request.user
#         quote.book = book
#         quote.save()
        
#         # Render the new quote
#         quote_html = render_to_string(
#             'books/partials/quote_item.html',
#             {'quote': quote, 'user': request.user}
#         )
        
#         return JsonResponse({
#             'success': True,
#             'quote_html': quote_html,
#             'quote_id': quote.id
#         })
#     else:
#         errors = {field: errors for field, errors in form.errors.items()}
#         return JsonResponse({'success': False, 'errors': errors}, status=400)


# @require_POST
# @login_required
# def filter_library(request):
#     """AJAX view to filter books in user library."""
#     status_filter = request.POST.get('status', 'all')
#     sort_by = request.POST.get('sort_by', '-last_read_date')
    
#     statuses = ReadingStatus.objects.filter(user=request.user)
    
#     if status_filter != 'all':
#         statuses = statuses.filter(status=status_filter)
    
#     statuses = statuses.select_related('book').order_by(sort_by)
    
#     html = render_to_string(
#         'books/partials/library_books.html',
#         {'statuses': statuses, 'user': request.user}
#     )
    
#     return JsonResponse({
#         'success': True,
#         'html': html,
#         'count': statuses.count()
#     })