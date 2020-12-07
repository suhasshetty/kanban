from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Category (models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Task ( models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField()
    updated_date = models.DateTimeField()