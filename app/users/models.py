from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Visitor(models.Model):
    target_user = models.OneToOneField(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.target_user.username} - {self.session_key}"