from rest_framework import serializers
from .models import Genre, Book, UserBookStatus, ReadingDiaryEntry, Quote

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class UserBookStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBookStatus
        fields = '__all__'

class DiaryEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingDiaryEntry
        fields = '__all__'

class QuoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = '__all__'
