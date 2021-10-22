from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from datetime import date

# Create your models here.

class User(AbstractUser):
	# contact = models.ForeignKey("Contact", on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(default='default.jpg', upload_to='profile_pics')
	pass


class Contact(models.Model):
	name = models.CharField(max_length=120)
	description = models.CharField(max_length=280, null=False, blank=False) # About
	phone_number = PhoneNumberField(null=False, blank=False)
	second_number = PhoneNumberField(null=True, blank=True)
	last_interaction_on = models.DateTimeField(blank=True, null=True)
	email = models.EmailField(max_length=254)
	job_title = models.CharField(max_length=120, blank=True, null=True)
	company = models.CharField(max_length=120, blank=True, null=True)
	country = models.CharField(max_length=120, blank=True, null=True)
	address = models.CharField(max_length=240, blank=True, null=True)
	twitter = models.URLField(max_length=120, default='None', blank=True, null=True)
	facebook = models.URLField(max_length=120, default='None', blank=True, null=True)
	instagram = models.URLField(max_length=120, default='None', blank=True, null=True)
	linkedin = models.URLField(max_length=120, default='None', blank=True, null=True)
	user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
	image = models.ImageField(default='default.jpg', upload_to='contact_pics')

	def __str__(self):
		return f"{self.name}"

	def serialize(self):
		return {
			"id": self.id,
			"description": self.description,
		}

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

	def serialize(self):
		return {
			"id": self.id,
			"body": self.body,
		}

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

	def serialize(self):
		return {
			"id": self.id,
			"body": self.body
		}

class Event(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	contact = models.ForeignKey(Contact, on_delete=models.CASCADE)
	date = models.DateField(default=date.today)
	details = models.CharField(max_length=280)
