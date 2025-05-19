# Register your models here.
from django.contrib import admin
from .models import Genre, Author, Book, BookReview, ReadingStatus


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['title', 'status', 'release_year', 'created']
    list_filter = ['status', 'created', 'authors', 'genres']
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ['title', 'description']
    date_hierarchy = 'created'
    filter_horizontal = ['authors', 'genres']


@admin.register(BookReview)
class BookReviewAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'rating', 'created']
    list_filter = ['rating', 'created']
    search_fields = ['comment', 'user__username', 'book__title']
    date_hierarchy = 'created'


@admin.register(ReadingStatus)
class ReadingStatusAdmin(admin.ModelAdmin):
    list_display = ['user', 'book', 'status', 'progress', 'last_read_date']
    list_filter = ['status', 'last_read_date']
    search_fields = ['user__username', 'book__title']
    date_hierarchy = 'last_read_date'