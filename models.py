from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Todo(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    date = models.DateField(default=timezone.localdate) 

    def __str__(self):
        return self.title