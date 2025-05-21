from rest_framework.routers import DefaultRouter
from .views import GenreViewSet, BookViewSet, UserBookStatusViewSet, DiaryEntryViewSet, QuoteViewSet

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'books', BookViewSet)
router.register(r'statuses', UserBookStatusViewSet)
router.register(r'diary', DiaryEntryViewSet)
router.register(r'quotes', QuoteViewSet)

urlpatterns = router.urls
