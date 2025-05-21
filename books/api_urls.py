# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import api_views

# # Create a router and register our viewsets with it
# router = DefaultRouter()
# router.register(r'books', api_views.BookViewSet)
# router.register(r'authors', api_views.AuthorViewSet)
# router.register(r'genres', api_views.GenreViewSet)
# router.register(r'publishers', api_views.PublisherViewSet)
# router.register(r'reviews', api_views.BookReviewViewSet)
# router.register(r'reading-statuses', api_views.ReadingStatusViewSet, basename='readingstatus')
# router.register(r'diary-entries', api_views.BookDiaryEntryViewSet, basename='bookdiaryentry')
# router.register(r'quotes', api_views.BookQuoteViewSet, basename='bookquote')

# # Wire up our API using automatic URL routing
# urlpatterns = [
#     path('', include(router.urls)),
#     path('my-library/', api_views.UserBookLibraryView.as_view(), name='api-my-library'),
#     path('reading-stats/', api_views.reading_stats, name='api-reading-stats'),
#     path('recommendations/', api_views.book_recommendations, name='api-recommendations'),
#     path('toggle-status/', api_views.toggle_reading_status, name='api-toggle-status'),
#     path('profile/', api_views.UserProfileView.as_view(), name='api-profile'),
# ]