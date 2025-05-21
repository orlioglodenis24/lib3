# from rest_framework import serializers
# from django.contrib.auth.models import User
# from django.db.models import Avg
# from .models import (
#     Book, Author, Genre, Publisher, BookReview,
#     ReadingStatus, BookDiaryEntry, BookQuote
# )


# class UserSerializer(serializers.ModelSerializer):
#     """Serializer for User model."""
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
#         read_only_fields = ['id', 'username', 'date_joined']


# class GenreSerializer(serializers.ModelSerializer):
#     """Serializer for Genre model."""
#     class Meta:
#         model = Genre
#         fields = ['id', 'name', 'slug', 'description']


# class AuthorSerializer(serializers.ModelSerializer):
#     """Serializer for Author model."""
#     class Meta:
#         model = Author
#         fields = ['id', 'name', 'slug', 'bio', 'photo']


# class PublisherSerializer(serializers.ModelSerializer):
#     """Serializer for Publisher model."""
#     class Meta:
#         model = Publisher
#         fields = ['id', 'name', 'slug']


# class BookReviewSerializer(serializers.ModelSerializer):
#     """Serializer for BookReview model."""
#     user = UserSerializer(read_only=True)
#     username = serializers.CharField(source='user.username', read_only=True)
    
#     class Meta:
#         model = BookReview
#         fields = ['id', 'book', 'user', 'username', 'rating', 'comment', 'created', 'updated']
#         read_only_fields = ['user', 'created', 'updated']


# class BookSerializer(serializers.ModelSerializer):
#     """Serializer for Book model with basic information."""
#     authors = serializers.StringRelatedField(many=True)
#     genres = serializers.StringRelatedField(many=True)
#     publisher = serializers.StringRelatedField()
#     average_rating = serializers.SerializerMethodField()
    
#     class Meta:
#         model = Book
#         fields = [
#             'id', 'title', 'slug', 'authors', 'genres', 'cover',
#             'status', 'release_year', 'created', 'updated',
#             'publisher', 'average_rating', 'age_restriction'
#         ]
#         read_only_fields = ['slug', 'created', 'updated']
    
#     def get_average_rating(self, obj):
#         """Calculate and return the average rating for a book."""
#         avg = obj.reviews.aggregate(Avg('rating'))['rating__avg']
#         return round(avg, 2) if avg else None


# class BookDetailSerializer(BookSerializer):
#     """Detailed serializer for Book model."""
#     authors = AuthorSerializer(many=True, read_only=True)
#     genres = GenreSerializer(many=True, read_only=True)
#     publisher = PublisherSerializer(read_only=True)
#     reviews = BookReviewSerializer(many=True, read_only=True)
    
#     class Meta(BookSerializer.Meta):
#         fields = BookSerializer.Meta.fields + [
#             'description', 'page_count', 'book_file', 'reviews'
#         ]


# class ReadingStatusSerializer(serializers.ModelSerializer):
#     """Serializer for ReadingStatus model."""
#     book = BookSerializer(read_only=True)
#     book_id = serializers.PrimaryKeyRelatedField(
#         queryset=Book.objects.all(), 
#         write_only=True,
#         source='book'
#     )
#     status_display = serializers.CharField(source='get_status_display', read_only=True)
    
#     class Meta:
#         model = ReadingStatus
#         fields = [
#             'id', 'book', 'book_id', 'status', 'status_display',
#             'start_date', 'end_date', 'last_read_date', 'progress'
#         ]
#         read_only_fields = ['last_read_date']


# class BookDiaryEntrySerializer(serializers.ModelSerializer):
#     """Serializer for BookDiaryEntry model."""
#     book = BookSerializer(read_only=True)
#     book_id = serializers.PrimaryKeyRelatedField(
#         queryset=Book.objects.all(), 
#         write_only=True,
#         source='book'
#     )
    
#     class Meta:
#         model = BookDiaryEntry
#         fields = [
#             'id', 'book', 'book_id', 'overall_rating',
#             'plot_originality', 'character_development', 'world_building',
#             'romance', 'humor', 'meaning_depth', 'emotions', 'summary',
#             'created', 'updated'
#         ]
#         read_only_fields = ['created', 'updated']


# class BookQuoteSerializer(serializers.ModelSerializer):
#     """Serializer for BookQuote model."""
#     book = BookSerializer(read_only=True)
#     book_id = serializers.PrimaryKeyRelatedField(
#         queryset=Book.objects.all(), 
#         write_only=True,
#         source='book'
#     )
    
#     class Meta:
#         model = BookQuote
#         fields = ['id', 'book', 'book_id', 'text', 'page_number', 'created']
#         read_only_fields = ['created']


# class UserBookLibrarySerializer(serializers.ModelSerializer):
#     """Serializer for user's book library."""
#     books = serializers.SerializerMethodField()
    
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'books']
    
#     def get_books(self, obj):
#         """Return books in user's library with reading status."""
#         reading_statuses = ReadingStatus.objects.filter(user=obj).select_related('book')
#         return [{
#             'status': status.status,
#             'status_display': status.get_status_display(),
#             'progress': status.progress,
#             'book': BookSerializer(status.book).data
#         } for status in reading_statuses]