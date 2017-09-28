from django.db import models
from django.contrib.auth.models import User
from department.models import Departament
from django.contrib.postgres.fields import ArrayField
# Create your models here.

class Logeado(models.Model):
    user = models.ForeignKey(User, null=False, blank=True, on_delete=models.CASCADE)
    avatar = models.CharField(max_length=200)
    departament = models.CharField(max_length=30)
    new = models.BooleanField(default=False)
    online = models.BooleanField(default=False)
    set_departament=models.IntegerField(null=False)

    def __str__(self):
        return '{}'.format(self.user.username)