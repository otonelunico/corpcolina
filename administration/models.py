from django.db import models
from authentication.models import Logeado

# Create your models here.

class Req(models.Model):
    user = models.ForeignKey(Logeado,null=False, blank=True, on_delete=models.CASCADE, unique=True)
    docs = models.BooleanField(default=False)
    tick = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    dpts = models.CharField(max_length=100)
    coment = models.TextField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
