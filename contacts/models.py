from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date

# Create your models here.

class User(AbstractUser):
	# contact = models.ForeignKey("Contact", on_delete=models.CASCADE, blank=True, null=True)
	pass

class Contact(models.Model):
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=280, null=False, blank=False)
	phone_number = PhoneNumberField(null=False, blank=False)
	second_number = PhoneNumberField(null=True, blank=True)
	last_interaction_on = models.DateTimeField(blank=True, null=True)
	email = models.EmailField(max_length=254)
	job_title = models.CharField(max_length=120, blank=True, null=True)
	company = models.CharField(max_length=120, blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)

	def __str__(self):
		return f"{self.name}"

# class Interaction(models.Model):
# 	title = models.CharField(max_length=120)
# 	description = models.CharField(max_length=280)
# 	was_at = models.DateTimeField(auto_now_add=True)
# 	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
# 	user = models.ForeignKey(User, on_delete=models.CASCADE)

# 	def __str__(self):
# 		return f"{self.title}: {self.was_at}"

class Note(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	date = models.DateField(default=date.today)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	body = models.TextField()

	def __str__(self):
		return f"{self.date}"

class Interaction(models.Model):
	INTERACTION_TYPES = (
		("call", "Phone Call"),
		("act", "Activity"),
		("rem", "Reminder")
	)

	user = models.ForeignKey(User, on_delete=models.CASCADE)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	date = models.DateField(default=date.today)
	body = models.CharField(max_length=280)
	type = models.CharField(max_length=5, choices=INTERACTION_TYPES, default="call")

	def __str__(self):
		return f"{self.type}: {self.contact.name} on {self.date}"