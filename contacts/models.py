from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.

class User(AbstractUser):
	pass

class Contact(models.Model):
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=280)
	phone_number = PhoneNumberField(unique=True, null=False, blank=False)
	second_number = PhoneNumberField(null=True, blank=True)
	last_interaction_on = models.DateTimeField(blank=True, null=True)
	email = models.EmailField(max_length=254)

	def __str__(self):
		return f"{self.name}"

class Interaction(models.Model):
	title = models.CharField(max_length=120)
	description = models.CharField(max_length=280)
	was_at = models.DateTimeField(auto_now_add=True)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.title}: {self.was_at}"