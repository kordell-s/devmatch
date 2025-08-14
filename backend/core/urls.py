"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from core.views import home
from accounts.views import register_view
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth.views import LoginView, LogoutView
from profiles.views import developer_search_ajax

urlpatterns = [
    path('', home, name='home'),  # Home view
    path("admin/", admin.site.urls),

    # Authentication URLs
    path('login/', LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', register_view, name='register'),  # Register view

    # API URLs
    path('api/accounts/', include('accounts.urls')),
    path('api/watchlist/', include('watchlist.urls')),
    path('api/projects/', include('projects.urls')),
    path('api/profiles/', include('profiles.urls')),
    path('api/developers/search/', developer_search_ajax, name='developer-search-ajax'),

    # HTML template views
    path('developers/', include('profiles.urls')),
    path('watchlist/', include('watchlist.urls')),

    # JWT login/refresh
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
