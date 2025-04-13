"""
URL configuration for kniharium project.

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

from accounts.views import SubmittableLoginView, user_logout, SignUpView, ProfileDetailView
from viewer.views import *

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', home_view, name='home'),
    path('books/', BooksListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book'),
    path('authors/', AuthorsListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author'),
    path('publishers/', PublishersListView.as_view(), name='publishers'),
    path('publisher/<int:pk>/', PublisherDetailView.as_view(), name='publisher'),
    path('about/', about, name='about'),

    path('accounts/login/', SubmittableLoginView.as_view(), name='login'),
    path('accounts/logout/', user_logout, name='logout'),
    # ostatní defaultní cesty
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('profile/<int:pk>/', ProfileDetailView.as_view(), name='profile'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)