from django.urls import path

from book.views import BookListView

urlpatterns = [
    path('book-list/', BookListView.as_view(), name='book-list'),
]
