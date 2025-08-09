from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WatchlistViewSet, watchlist_view

router = DefaultRouter()
router.register(r'watchlists', WatchlistViewSet, basename='watchlist')

urlpatterns = [
    path('view/', watchlist_view, name='watchlist-view'),  # Add the watchlist view
    path('', include(router.urls)),  # Include the router URLs
]