from django.contrib import admin
from .models import User, Contact, Interaction

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Interaction)
