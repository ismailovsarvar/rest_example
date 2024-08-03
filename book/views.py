from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from book.models import Book


# Create your views here.

class BookListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        book_data = [
            {
                'name': book.name,
                'description': book.description,
                'author': book.author,
                'price': book.price
            }
            for book in Book.objects.all()]
        return Response(book_data, status=status.HTTP_200_OK)
