from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import BookReview, ReadingStatus, Genre


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
    
    class Meta:
        model = ReadingStatus
        fields = ['status', 'progress']


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