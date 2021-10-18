from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Contact, User

# Create your views here.

def index(request):
	return render(request, "contacts/landing/index.html")

# User and authentication views
def login_view(request):
	if request.method == "POST":

		# Attempt to sign user in
		username = request.POST["username"]
		password = request.POST["password"]
		user = authenticate(request, username=username, password=password)

		# Check if authentication was successful
		if user is not None:
			login(request, user)
			return HttpResponseRedirect(reverse("dashboard"))
		else:
			return render(request, "contacts/landing/login.html", {
				"message": "Invalid username and/or password."
			})

	else:
		return render(request, "contacts/landing/login.html")


def logout_view(request):
	logout(request)
	return HttpResponseRedirect(reverse("index"))

def register(request):
	if request.method == "POST":
		username = request.POST["username"]
		email = request.POST["email"]

		# Ensure password matches confirmation
		password = request.POST["password"]
		confirmation = request.POST["confirmation"]
		if password != confirmation:
			return render(request, "contacts/landing/register.html", {
				"message": "Passwords must match."
			})

		# Attempt to create new user
		try:
			user = User.objects.create_user(username, email, password)
			user.save()
		except IntegrityError:
			return render(request, "contacts/landing/register.html", {
				"message": "Username already taken."
			})
		login(request, user)
		return HttpResponseRedirect(reverse("dashboard"))
	else:
		return render(request, "contacts/landing/register.html")


# Data views

@login_required
def dashboard(request):
	return render(request, "contacts/dashboard/dashboard.html")

@login_required
def contacts(request):
	user = request.user
	# contacts = User.objects.filter(username=user.username).values('contact').all()
	# contacts = Contact.objects.filter(user=user).all()
	contacts = Contact.objects.filter(user=user).order_by('name')
	print(contacts)
	return render(request, "contacts/contact-list.html", {
		"contacts": contacts
	})

@login_required
def contact(request, contact_id):
	person = Contact.objects.get(pk=contact_id)
	print(person)
	return render(request, 'contacts/contact.html', {
		"person": person
	})

@login_required
def meetings(request):
	return render(request, "contacts/meetings.html")
