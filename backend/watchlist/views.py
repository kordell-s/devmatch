from rest_framework import viewsets, permissions
from .models import Watchlist
from .serializer import WatchlistSerializer

# Create your views here.


class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Watchlist.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise permissions.PermissionDenied("You must be logged in to create a watchlist item.")
        serializer.save(user=self.request.user)
