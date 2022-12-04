from rest_framework import serializers

from applications.book.models import Book


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.CharField(required=False)

    class Meta:
        model = Book
        fields = '__all__'

    def create(self, validated_data):
        owner = self.context.get('request').user
        book = Book.objects.create(owner=owner, **validated_data)
        return book
