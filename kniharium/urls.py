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
    path('book/create/', BookCreateView.as_view(), name='book_create'),
    path('book/update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('book/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),

    path('authors/', AuthorsListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author'),
    path('author/create/', AuthorCreateView.as_view(), name='author_create'),
    path('author/update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),
    path('author/delete/<int:pk>/', AuthorDeleteView.as_view(), name='author_delete'),

    path('publishers/', PublishersListView.as_view(), name='publishers'),
    path('publisher/<int:pk>/', PublisherDetailView.as_view(), name='publisher'),
    path('publisher/create/', PublisherCreateView.as_view(), name='publisher_create'),
    path('publisher/update/<int:pk>/', PublisherUpdateView.as_view(), name='publisher_update'),
    path('publisher/delete/<int:pk>/', PublisherDeleteView.as_view(), name='publisher_delete'),

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