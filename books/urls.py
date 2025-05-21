from django.urls import path
from . import views
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("", views.index, name="index"),
    path("books/", views.book_list, name="book_list"),
    # path("books/<slug:slug>/", views.book_detail, name="book_detail"),
    # path("authors/<slug:slug>/", views.author_detail, name="author_detail"),
    # path("genres/<slug:slug>/", views.genre_detail, name="genre_detail"),
    # path("update-reading-status/<int:book_id>/", views.update_reading_status, name="update_reading_status"),
    # path("update-progress/<int:status_id>/", views.update_progress, name="update_progress"),
    # path("my-library/", views.my_library, name="my_library"),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('register/', views.register, name='register'),
]


# from django.urls import path, include
# from . import views

# urlpatterns = [
#     # Основные страницы
#     path("", views.index, name="index"),
#     path("books/", views.book_list, name="book_list"),
#     path("books/<slug:slug>/", views.book_detail, name="book_detail"),
#     path("authors/<slug:slug>/", views.author_detail, name="author_detail"),
#     path("genres/<slug:slug>/", views.genre_detail, name="genre_detail"),
    
#     # Управление статусом чтения
#     path("update-reading-status/<int:book_id>/", views.update_reading_status, name="update_reading_status"),
#     path("update-progress/<int:status_id>/", views.update_progress, name="update_progress"),
    
#     # Библиотека пользователя и профиль
#     path("my-library/", views.my_library, name="my_library"),
#     path("profile/", views.user_profile, name="user_profile"),
    
#     # Управление рецензиями, дневниками и цитатами
#     path("add-review/<int:book_id>/", views.add_book_review, name="add_book_review"),
#     path("add-diary-entry/<int:book_id>/", views.add_diary_entry, name="add_diary_entry"),
#     path("add-quote/<int:book_id>/", views.add_book_quote, name="add_book_quote"),
#     path("delete-quote/<int:quote_id>/", views.delete_book_quote, name="delete_book_quote"),
    
#     # Управление книгами
#     path("add-book/", views.add_book, name="add_book"),
#     path("edit-book/<int:book_id>/", views.edit_book, name="edit_book"),
#     path("delete-book/<int:book_id>/", views.delete_book, name="delete_book"),
    
#     # Аутентификация
#     path('accounts/', include('django.contrib.auth.urls')),
#     path('register/', views.register, name='register'),


#     path('api/', include('books.api_urls')),
#     path('api-auth/', include('rest_framework.urls')),
#     path('docs/', include_docs_urls(title='BookDiary API')),
# ]