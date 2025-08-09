from rest_framework import viewsets, permissions
from .models import Watchlist
from .serializer import WatchlistSerializer
from django.shortcuts import render

# Create your views here.

class WatchlistViewSet(viewsets.ModelViewSet):
    serializer_class = WatchlistSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def get_queryset(self):
        return Watchlist.objects.filter(recruiter=self.request.user)

    def perform_create(self, serializer):
        if not self.request.user.is_authenticated:
            raise permissions.PermissionDenied("You must be logged in to create a watchlist item.")
        serializer.save(recruiter=self.request.user)

#function based view

def watchlist_view(request):
    if not request.user.is_authenticated:
        return render(request, '403.html', status=403)
    watchlist_items = Watchlist.objects.filter(recruiter=request.user)
    return render(request, 'watchlist/watchlist.html', {'watchlist_items': watchlist_items})
