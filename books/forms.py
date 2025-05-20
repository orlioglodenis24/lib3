from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import BookReview, ReadingStatus, Genre, Publisher, Author
from .models import Book, BookDiaryEntry, BookQuote


class BookReviewForm(forms.ModelForm):
    """Form for users to add and edit book reviews."""
    rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '10',
            'step': '1'
        })
    )
    
    comment = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'review-textarea',
            'placeholder': 'Write your review here...',
            'rows': 5
        })
    )
    
    class Meta:
        model = BookReview
        fields = ['rating', 'comment']


class ReadingStatusForm(forms.ModelForm):
    """Form for users to update their reading status for a book."""
    status = forms.ChoiceField(
        choices=ReadingStatus.STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'status-select'})
    )
    
    progress = forms.IntegerField(
        required=False,
        min_value=0,
        widget=forms.NumberInput(attrs={
            'class': 'progress-input',
            'min': '0',
            'step': '1'
        })
    )
    
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'date-input',
            'type': 'date'
        })
    )
    
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'date-input',
            'type': 'date'
        })
    )
    
    class Meta:
        model = ReadingStatus
        fields = ['status', 'progress', 'start_date', 'end_date']


class BookSearchForm(forms.Form):
    """Form for searching and filtering books."""
    SORT_CHOICES = (
        ('-created', 'Latest Added'),
        ('title', 'Title A-Z'),
        ('-title', 'Title Z-A'),
        ('-reviews__rating', 'Highest Rated'),
        ('release_year', 'Release Year (Oldest)'),
        ('-release_year', 'Release Year (Newest)'),
    )
    
    query = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'search-input',
            'placeholder': 'Search books...'
        })
    )
    
    genre = forms.ModelChoiceField(
        queryset=Genre.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    
    status = forms.ChoiceField(
        choices=(('', 'All Status'),) + Book.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )
    
    sort = forms.ChoiceField(
        choices=SORT_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'sort-select'})
    )


class BookDiaryEntryForm(forms.ModelForm):
    """Form for users to create and edit book diary entries with detailed ratings."""
    overall_rating = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    plot_originality = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    character_development = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    world_building = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    romance = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    humor = forms.IntegerField(
        required=False,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    meaning_depth = forms.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        widget=forms.NumberInput(attrs={
            'class': 'rating-input',
            'min': '1',
            'max': '5',
            'step': '1'
        })
    )
    
    emotions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'diary-textarea',
            'placeholder': 'Describe your emotions while reading this book...',
            'rows': 3
        })
    )
    
    summary = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'diary-textarea',
            'placeholder': 'Write your personal summary or notes about this book...',
            'rows': 5
        })
    )
    
    class Meta:
        model = BookDiaryEntry
        fields = [
            'overall_rating', 'plot_originality', 'character_development', 
            'world_building', 'romance', 'humor', 'meaning_depth',
            'emotions', 'summary'
        ]


class BookQuoteForm(forms.ModelForm):
    """Form for users to add book quotes."""
    text = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'quote-textarea',
            'placeholder': 'Add a memorable quote from the book...',
            'rows': 3
        })
    )
    
    page_number = forms.IntegerField(
        required=False,
        min_value=1,
        widget=forms.NumberInput(attrs={
            'class': 'page-input',
            'min': '1',
            'step': '1',
            'placeholder': 'Page number (optional)'
        })
    )
    
    class Meta:
        model = BookQuote
        fields = ['text', 'page_number']


class BookUploadForm(forms.ModelForm):
    """Form for users to upload their own books."""
    title = forms.CharField(max_length=200)
    cover = forms.ImageField(required=False)
    book_file = forms.FileField(required=False)
    description = forms.CharField(
        widget=forms.Textarea(attrs={
            'rows': 5,
            'placeholder': 'Add book description/annotation here...'
        })
    )
    
    authors = forms.ModelMultipleChoiceField(
        queryset=Author.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )
    
    new_author = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Add new author if not in the list'})
    )
    
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'select2'})
    )
    
    publisher = forms.ModelChoiceField(
        queryset=Publisher.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'select2'})
    )
    
    new_publisher = forms.CharField(
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Add new publisher if not in the list'})
    )
    
    release_year = forms.IntegerField(required=False)
    page_count = forms.IntegerField(required=False)
    age_restriction = forms.ChoiceField(choices=Book.AGE_RESTRICTION_CHOICES)
    
    class Meta:
        model = Book
        fields = [
            'title', 'cover', 'book_file', 'description', 'authors', 
            'genres', 'publisher', 'release_year', 'page_count', 'age_restriction'
        ]