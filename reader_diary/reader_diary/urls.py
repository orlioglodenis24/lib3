from django.contrib import admin
from django.urls import path, include
from django.urls import path, include
from books.views import index
from books  import views

from django.conf import settings
from django.conf.urls.static import static
from books.models import Genre

urlpatterns = [
    path('', index, name='index'),
    path('books/', include('books.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('books.urls')),  
    path('profile/', views.profile, name='profile'),
    path('user/books/', views.user_books, name='user_books'),
    path('user/caralog/',views.catalog,name='catalog'),
    path('genres/', views.genres, name='genres'),
    path('diary/', views.diary, name='diary'),  
    path('profile/edit/', views.profile_edit, name='profile_edit'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('info/', views.genres_and_authors, name='genres_and_authors'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)