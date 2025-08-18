from rest_framework import viewsets, permissions
from .models import Watchlist
from .serializer import WatchlistSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from profiles.models import Developer
from django.http import JsonResponse
from django.contrib import messages

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

@login_required
def watchlist_view(request):
    if not request.user.is_authenticated:
        return render(request, '403.html', status=403)
    else:
        if request.user.role != 'recruiter':
            messages.error(request, "You must be a recruiter to view the watchlist.")
            return redirect('developers-list')
    watchlist_items = Watchlist.objects.filter(recruiter=request.user)
    return render(request, 'watchlist/watchlist.html', {'watchlist_items': watchlist_items})

@login_required
def add_to_watchlist(request, developer_id):
    if request.user.role != 'recruiter':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Only recruiters can add developers to their watchlist.'})
        messages.error(request, "Only recruiters can add developers to their watchlist.")
        return redirect('developer-detail', developer_id)
    
    developer = get_object_or_404(Developer, id=developer_id)

    if request.method == 'POST':
        watchlist_item, created = Watchlist.objects.get_or_create(
            recruiter=request.user,
            developer=developer
        )
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            if created:
                return JsonResponse({
                    'success': True, 
                    'message': f"{developer.user.get_full_name() or developer.user.username} has been added to your watchlist.",
                    'is_in_watchlist': True
                })
            else:
                return JsonResponse({
                    'success': True, 
                    'message': f"{developer.user.get_full_name() or developer.user.username} is already in your watchlist.",
                    'is_in_watchlist': True
                })
        
        if created:
            messages.success(request, f"{developer.user.get_full_name() or developer.user.username} has been added to your watchlist.")
        else:
            messages.info(request, f"{developer.user.get_full_name() or developer.user.username} is already in your watchlist.")
    
    return redirect('developer-detail', developer_id)

@login_required
def remove_from_watchlist(request, developer_id):
    if request.user.role != 'recruiter':
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Only recruiters can remove developers from their watchlist.'})
        messages.error(request, "Only recruiters can remove developers from their watchlist.")
        return redirect('developer-detail', developer_id)
    
    developer = get_object_or_404(Developer, id=developer_id)

    if request.method == 'POST':
        try:
            watchlist_item = Watchlist.objects.get(recruiter=request.user, developer=developer)
            watchlist_item.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True, 
                    'message': f"{developer.user.get_full_name() or developer.user.username} has been removed from your watchlist.",
                    'is_in_watchlist': False
                })
            
            messages.success(request, f"{developer.user.get_full_name() or developer.user.username} has been removed from your watchlist.")
        except Watchlist.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False, 
                    'message': f"{developer.user.get_full_name() or developer.user.username} is not in your watchlist.",
                    'is_in_watchlist': False
                })
            messages.error(request, f"{developer.user.get_full_name() or developer.user.username} is not in your watchlist.")
    
    return redirect('developer-detail', developer_id)

@login_required
def check_watchlist(request, developer_id):
    if request.user.role != 'recruiter':
        return JsonResponse({'success': False, 'message': 'Only recruiters can check watchlist status.'})
    
    developer = get_object_or_404(Developer, id=developer_id)
    is_in_watchlist = Watchlist.objects.filter(recruiter=request.user, developer=developer).exists()

    return JsonResponse({
        'success': True,
        'is_in_watchlist': is_in_watchlist,
        'developer_id': developer.id
    })