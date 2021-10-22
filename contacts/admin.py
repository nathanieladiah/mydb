from django.contrib import admin
from .models import User, Contact, Interaction, Note, Event

# Register your models here.
admin.site.register(User)
admin.site.register(Contact)
admin.site.register(Interaction)
admin.site.register(Note)
admin.site.register(Event)