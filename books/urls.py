from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.book_list, name="book_list"),
    path("books/<slug:slug>/", views.book_detail, name="book_detail"),
    path("authors/<slug:slug>/", views.author_detail, name="author_detail"),
    path("genres/<slug:slug>/", views.genre_detail, name="genre_detail"),
    path("update-reading-status/<int:book_id>/", views.update_reading_status, name="update_reading_status"),
    path("update-progress/<int:status_id>/", views.update_progress, name="update_progress"),
    path("my-library/", views.my_library, name="my_library"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]