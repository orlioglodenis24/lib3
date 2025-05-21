# from rest_framework import viewsets, permissions, status, generics, filters
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
# from rest_framework.pagination import PageNumberPagination
# from django.shortcuts import get_object_or_404
# from django.db.models import Avg, Count, Q
# from django.contrib.auth.models import User
# from django.utils.text import slugify

# from .models import (
#     Book, Author, Genre, Publisher, BookReview, 
#     ReadingStatus, BookDiaryEntry, BookQuote
# )
# from .serializers import (
#     BookSerializer, BookDetailSerializer, AuthorSerializer, 
#     GenreSerializer, PublisherSerializer, BookReviewSerializer,
#     ReadingStatusSerializer, BookDiaryEntrySerializer, BookQuoteSerializer,
#     UserSerializer
# )


# class StandardResultsSetPagination(PageNumberPagination):
#     """Custom pagination class for API views."""
#     page_size = 20
#     page_size_query_param = 'page_size'
#     max_page_size = 100


# class BookViewSet(viewsets.ModelViewSet):
#     """API endpoint for books."""
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer
#     detail_serializer_class = BookDetailSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter, filters.OrderingFilter]
#     search_fields = ['title', 'description', 'authors__name']
#     ordering_fields = ['title', 'created', 'release_year', 'reviews__rating']
#     ordering = ['-created']
    
#     def get_serializer_class(self):
#         if self.action == 'retrieve':
#             return self.detail_serializer_class
#         return self.serializer_class
    
#     def get_queryset(self):
#         queryset = Book.objects.all()
        
#         # Filter by genre
#         genre = self.request.query_params.get('genre', None)
#         if genre:
#             queryset = queryset.filter(genres__slug=genre)
        
#         # Filter by author
#         author = self.request.query_params.get('author', None)
#         if author:
#             queryset = queryset.filter(authors__slug=author)
        
#         # Filter by status
#         status_param = self.request.query_params.get('status', None)
#         if status_param:
#             queryset = queryset.filter(status=status_param)
        
#         # Filter by release year
#         year = self.request.query_params.get('year', None)
#         if year:
#             queryset = queryset.filter(release_year=year)
        
#         # Filter by age restriction
#         age = self.request.query_params.get('age', None)
#         if age:
#             queryset = queryset.filter(age_restriction__lte=age)
        
#         return queryset.distinct()
    
#     def perform_create(self, serializer):
#         """Save the book with the current user as added_by."""
#         serializer.save(added_by=self.request.user)


# class AuthorViewSet(viewsets.ModelViewSet):
#     """API endpoint for authors."""
#     queryset = Author.objects.all()
#     serializer_class = AuthorSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = StandardResultsSetPagination
#     filter_backends = [filters.SearchFilter]
#     search_fields = ['name', 'bio']
    
#     def perform_create(self, serializer):
#         """Automatically generate slug from name if not provided."""
#         if not serializer.validated_data.get('slug'):
#             name = serializer.validated_data.get('name')
#             serializer.save(slug=slugify(name))
#         else:
#             serializer.save()


# class GenreViewSet(viewsets.ModelViewSet):
#     """API endpoint for genres."""
#     queryset = Genre.objects.all()
#     serializer_class = GenreSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = StandardResultsSetPagination
    
#     def perform_create(self, serializer):
#         """Automatically generate slug from name if not provided."""
#         if not serializer.validated_data.get('slug'):
#             name = serializer.validated_data.get('name')
#             serializer.save(slug=slugify(name))
#         else:
#             serializer.save()


# class PublisherViewSet(viewsets.ModelViewSet):
#     """API endpoint for publishers."""
#     queryset = Publisher.objects.all()
#     serializer_class = PublisherSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = StandardResultsSetPagination
    
#     def perform_create(self, serializer):
#         """Automatically generate slug from name if not provided."""
#         if not serializer.validated_data.get('slug'):
#             name = serializer.validated_data.get('name')
#             serializer.save(slug=slugify(name))
#         else:
#             serializer.save()


# class BookReviewViewSet(viewsets.ModelViewSet):
#     """API endpoint for book reviews."""
#     queryset = BookReview.objects.all()
#     serializer_class = BookReviewSerializer
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = StandardResultsSetPagination
    
#     def get_queryset(self):
#         """Filter reviews by book if book_id parameter is provided."""
#         queryset = BookReview.objects.all()
#         book_id = self.request.query_params.get('book', None)
#         if book_id:
#             queryset = queryset.filter(book_id=book_id)
#         return queryset
    
#     def perform_create(self, serializer):
#         """Save the review with the current user."""
#         serializer.save(user=self.request.user)


# class ReadingStatusViewSet(viewsets.ModelViewSet):
#     """API endpoint for reading statuses."""
#     serializer_class = ReadingStatusSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """Return reading statuses for the current user."""
#         if getattr(self, 'swagger_fake_view', False):
#             # Return empty queryset for OpenAPI schema generation
#             return ReadingStatus.objects.none()
        
#         return ReadingStatus.objects.filter(user=self.request.user)
    
#     def perform_create(self, serializer):
#         """Save the reading status with the current user."""
#         serializer.save(user=self.request.user)


# class BookDiaryEntryViewSet(viewsets.ModelViewSet):
#     """API endpoint for book diary entries."""
#     serializer_class = BookDiaryEntrySerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """Return diary entries for the current user."""
#         if getattr(self, 'swagger_fake_view', False):
#             return BookDiaryEntry.objects.none()
            
#         return BookDiaryEntry.objects.filter(user=self.request.user)
    
#     def perform_create(self, serializer):
#         """Save the diary entry with the current user."""
#         serializer.save(user=self.request.user)


# class BookQuoteViewSet(viewsets.ModelViewSet):
#     """API endpoint for book quotes."""
#     serializer_class = BookQuoteSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """Return quotes for the current user or filter by book."""
#         if getattr(self, 'swagger_fake_view', False):
#             return BookQuote.objects.none()
            
#         queryset = BookQuote.objects.filter(user=self.request.user)
#         book_id = self.request.query_params.get('book', None)
#         if book_id:
#             queryset = queryset.filter(book_id=book_id)
#         return queryset
    
#     def perform_create(self, serializer):
#         """Save the quote with the current user."""
#         serializer.save(user=self.request.user)


# class UserBookLibraryView(generics.ListAPIView):
#     """API endpoint for a user's book library."""
#     serializer_class = ReadingStatusSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_queryset(self):
#         """Return reading statuses for the current user."""
#         if getattr(self, 'swagger_fake_view', False):
#             return ReadingStatus.objects.none()
            
#         user = self.request.user
#         status_filter = self.request.query_params.get('status', None)
        
#         queryset = ReadingStatus.objects.filter(user=user)
#         if status_filter:
#             queryset = queryset.filter(status=status_filter)
        
#         return queryset.select_related('book')


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def reading_stats(request):
#     """API endpoint for user reading statistics."""
#     user = request.user
    
#     # Get total books by status
#     reading_count = ReadingStatus.objects.filter(user=user, status='reading').count()
#     completed_count = ReadingStatus.objects.filter(user=user, status='completed').count()
#     plan_count = ReadingStatus.objects.filter(user=user, status='plan_to_read').count()
#     dropped_count = ReadingStatus.objects.filter(user=user, status='dropped').count()
    
#     # Get total pages read
#     total_pages = ReadingStatus.objects.filter(
#         user=user, status='completed'
#     ).select_related('book').aggregate(
#         pages_sum=Sum('book__page_count')
#     )['pages_sum'] or 0
    
#     # Get favorite genres based on completed books
#     favorite_genres = Genre.objects.filter(
#         books__reading_statuses__user=user,
#         books__reading_statuses__status='completed'
#     ).annotate(
#         book_count=Count('books')
#     ).order_by('-book_count')[:5]
    
#     # Get average rating given by user
#     avg_rating = BookReview.objects.filter(
#         user=user
#     ).aggregate(
#         avg=Avg('rating')
#     )['avg'] or 0
    
#     return Response({
#         'reading_count': reading_count,
#         'completed_count': completed_count,
#         'plan_count': plan_count,
#         'dropped_count': dropped_count,
#         'total_pages': total_pages,
#         'favorite_genres': [
#             {'name': genre.name, 'count': genre.book_count} 
#             for genre in favorite_genres
#         ],
#         'average_rating': round(avg_rating, 1),
#     })


# @api_view(['GET'])
# def book_recommendations(request):
#     """API endpoint for book recommendations."""
#     if not request.user.is_authenticated:
#         # For anonymous users, return popular books
#         popular_books = Book.objects.annotate(
#             avg_rating=Avg('reviews__rating'),
#             review_count=Count('reviews')
#         ).filter(review_count__gt=0).order_by('-avg_rating')[:10]
        
#         serializer = BookSerializer(popular_books, many=True)
#         return Response(serializer.data)
    
#     # For authenticated users, provide personalized recommendations
#     user = request.user
    
#     # Find genres the user has read
#     user_genres = Genre.objects.filter(
#         books__reading_statuses__user=user
#     ).distinct()
    
#     # Find books in those genres that the user hasn't read yet
#     recommended_books = Book.objects.filter(
#         genres__in=user_genres
#     ).exclude(
#         reading_statuses__user=user
#     ).annotate(
#         avg_rating=Avg('reviews__rating')
#     ).order_by('-avg_rating')[:10]
    
#     serializer = BookSerializer(recommended_books, many=True)
#     return Response(serializer.data)


# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def toggle_reading_status(request):
#     """Quick API endpoint to toggle a book's reading status."""
#     book_id = request.data.get('book_id')
#     new_status = request.data.get('status')
    
#     if not book_id or not new_status:
#         return Response(
#             {'error': 'Book ID and status are required'}, 
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
#     valid_statuses = [choice[0] for choice in ReadingStatus.STATUS_CHOICES]
#     if new_status not in valid_statuses:
#         return Response(
#             {'error': f'Invalid status. Must be one of: {", ".join(valid_statuses)}'}, 
#             status=status.HTTP_400_BAD_REQUEST
#         )
    
#     book = get_object_or_404(Book, id=book_id)
    
#     # Get or create reading status
#     reading_status, created = ReadingStatus.objects.get_or_create(
#         user=request.user,
#         book=book,
#         defaults={'status': new_status}
#     )
    
#     if not created:
#         reading_status.status = new_status
#         reading_status.save()
    
#     serializer = ReadingStatusSerializer(reading_status)
#     return Response(serializer.data)


# class UserProfileView(generics.RetrieveUpdateAPIView):
#     """API endpoint for user profile."""
#     serializer_class = UserSerializer
#     permission_classes = [IsAuthenticated]
    
#     def get_object(self):
#         return self.request.user