from django.contrib import admin
from documents.models import Document, Document_type, Receiver,Remittent
# Register your models here.
admin.site.register(Document)
admin.site.register(Document_type)
admin.site.register(Remittent)
admin.site.register(Receiver)