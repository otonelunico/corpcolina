from django.db import models
from django.contrib.auth.models import User
from department.models import Departament


class Communicators(models.Model):
    last_name = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    job_title = models.CharField(max_length=100)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Remittent(Communicators):
    signature = models.TextField()

    def __str__(self):

        return (self.last_name + " " + self.first_name)


class Receiver(Communicators):

    def __str__(self):

        return (self.last_name + " " + self.first_name)


class Document_type(models.Model):
    titulo = models.CharField(max_length=50)

    def __str__(self):

        return self.titulo

class Document(models.Model):
    type = models.ForeignKey(Document_type, null=False, blank=True, on_delete=models.CASCADE)
    number = models.IntegerField(null=False)
    matter = models.CharField(max_length=50, null=False)
    previous = models.CharField(max_length=50, null=False)
    receiver = models.ForeignKey(Receiver, null=False, blank=True, on_delete=models.CASCADE)
    remittent = models.ForeignKey(Remittent, null=False, blank=True, on_delete=models.CASCADE)
    body = models.TextField(null=False)
    footer = models.TextField(null=False)
    year = models.TextField()
    user = models.ForeignKey(User, null=False, blank= True, on_delete=models.CASCADE)
    departament = models.ForeignKey(Departament, null=False, blank=True, on_delete=models.CASCADE)
    activo = models.BooleanField(default=True)
    print = models.BooleanField(default=False)
    send = models.BooleanField(default=False)
    change = models.BooleanField()
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Alertmessage(models.Model):
    type = models.CharField(max_length=50, null=True)
    message = models.CharField(max_length=50, null=True)
    asign = models.IntegerField(null=True)

    def __str__(self):
        return self.message
