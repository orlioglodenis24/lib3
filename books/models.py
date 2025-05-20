from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator


class Genre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('genre_detail', args=[self.slug])


class Author(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to='authors/', blank=True, null=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('author_detail', args=[self.slug])


class Publisher(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name


class Book(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('hiatus', 'On Hiatus'),
        ('dropped', 'Dropped'),
    )
    
    AGE_RESTRICTION_CHOICES = (
        (0, 'All Ages'),
        (6, '6+'),
        (12, '12+'),
        (16, '16+'),
        (18, '18+'),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='ongoing')
    release_year = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    # Additional fields based on requirements
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True, related_name='books')
    page_count = models.PositiveIntegerField(null=True, blank=True)
    age_restriction = models.PositiveSmallIntegerField(choices=AGE_RESTRICTION_CHOICES, default=0)
    book_file = models.FileField(upload_to='book_files/', null=True, blank=True)
    added_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='added_books')
    
    class Meta:
        ordering = ['-updated']
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', args=[self.slug])
    
    def get_average_rating(self):
        reviews = self.reviews.all()
        if reviews:
            return sum(review.rating for review in reviews) / len(reviews)
        return 0


class BookReview(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])
    comment = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created']
        unique_together = ['book', 'user']
    
    def __str__(self):
        return f'Review by {self.user.username} for {self.book.title}'


class ReadingStatus(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Currently Reading'),
        ('completed', 'Completed'),
        ('plan_to_read', 'Plan to Read'),
        ('dropped', 'Dropped'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_statuses')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reading_statuses')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    last_read_date = models.DateField(default=timezone.now)
    progress = models.PositiveIntegerField(default=0, help_text="Progress in number of pages")
    
    class Meta:
        unique_together = ['user', 'book']
        verbose_name_plural = 'Reading statuses'
    
    def __str__(self):
        return f'{self.user.username} - {self.book.title}: {self.get_status_display()}'


class BookDiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='diary_entries')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='diary_entries')
    overall_rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    plot_originality = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    character_development = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    world_building = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    romance = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    humor = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], null=True, blank=True)
    meaning_depth = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    emotions = models.TextField(blank=True, help_text="Emotions experienced while reading")
    summary = models.TextField(blank=True, help_text="Brief summary or personal notes about the book")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated']
        unique_together = ['user', 'book']
        verbose_name_plural = 'Book diary entries'
    
    def __str__(self):
        return f'Diary entry by {self.user.username} for {self.book.title}'


class BookQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_quotes')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='quotes')
    text = models.TextField()
    page_number = models.PositiveIntegerField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created']
    
    def __str__(self):
        return f'Quote from {self.book.title}: {self.text[:50]}...'