from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Book(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books')

    def __str__(self):
        return self.title
