from django.db import models

# Create your models here.

class Departament(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    state = models.BooleanField(default=True)

    def __str__(self):

        return self.name