from django.shortcuts import render
from rest_framework import permissions, generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from applications.book.models import Book
from applications.book.serializers import BookSerializer


class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class BookRetrieveUpdateApiView(generics.RetrieveUpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


@api_view(['DELETE'])
def book_del_api_view(request, pk):
    try:
        book = Book.objects.get(id=pk)
        book_owner = book.owner
        user = request.user
        if book_owner == user:
            book.delete()
            return Response({'msg': 'Успешно удалено'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Удалить книгу может только ее автор'}, status=status.HTTP_400_BAD_REQUEST)
    except Book.DoesNotExist:
        return Response({'msg': 'Нет такой книги'}, status=status.HTTP_400_BAD_REQUEST)
