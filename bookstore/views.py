from rest_framework import viewsets
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Book, Author, Category
from .serializers import BookSerializer, AuthorSerializer, CategorySerializer

from django.shortcuts import render
import requests


class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    
    # Filter books by category and price range
    filterset_fields = ['category', 'price']
    
    # Search by book title or author name
    search_fields = ['title', 'author__name']
    
    # Order by rating or published date
    ordering_fields = ['rating', 'published_date', 'price']

class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer





def book_list_view(request):
    api_url = request.build_absolute_uri('/api/books/')
    
    params = {
        'category': request.GET.get('category', ''),
        'price_min': request.GET.get('price_min', ''),
        'price_max': request.GET.get('price_max', ''),
        'search': request.GET.get('search', ''),
        'ordering': request.GET.get('ordering', ''),
        'page': request.GET.get('page', 1),
    }
    
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()
        books_data = response.json()
    except requests.exceptions.RequestException as e:
        books_data = {'results': [], 'count': 0, 'next': None, 'previous': None}
        print(f"Error fetching data from API: {e}")

    return render(request, 'book_list.html', {'books_data': books_data})    