from django.db import models
from django.contrib.auth.models import User

class Author(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    publisher = models.CharField(max_length=255, blank=True)
    year = models.PositiveIntegerField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    age_limit = models.CharField(max_length=50, blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, null=True)
    annotation = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True)
    text_file = models.FileField(upload_to='texts/', blank=True, null=True)

    def __str__(self):
        return self.title

class UserBookStatus(models.Model):
    STATUS_CHOICES = (
        ('reading', 'Читаю'),
        ('read', 'Прочитал'),
        ('planned', 'В планах'),
        ('dropped', 'Брошено'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title} - {self.status}"

class ReadingDiaryEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    emotions_rating = models.PositiveSmallIntegerField(default=1)  # 1-5
    plot_originality = models.PositiveSmallIntegerField(default=1)  # 1-5
    character_development = models.PositiveSmallIntegerField(default=1)
    world_building = models.PositiveSmallIntegerField(default=1)
    romance = models.PositiveSmallIntegerField(default=1)
    humor = models.PositiveSmallIntegerField(default=1)
    meaning = models.PositiveSmallIntegerField(default=1)
    summary = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Diary entry by {self.user.username} for {self.book.title}"

class Quote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Quote by {self.user.username} for {self.book.title}"
