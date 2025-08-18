from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchlistViewSet, watchlist_view, add_to_watchlist, remove_from_watchlist, check_watchlist

router = DefaultRouter()
router.register(r'watchlists', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('view/', watchlist_view, name='watchlist-view'),
    path('add/<int:developer_id>/', add_to_watchlist, name='add-to-watchlist'),
    path('remove/<int:developer_id>/', remove_from_watchlist, name='remove-from-watchlist'),
    path('check/<int:developer_id>/', check_watchlist, name='check-watchlist'),
    path('', include(router.urls)),
]