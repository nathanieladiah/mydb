from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse

from .models import Contact, Interaction, User, Note

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
	return render(request, "contacts/dashboard/contactlist.html", {
		"contacts": contacts
	})

@login_required
def add_contact(request):
	if request.method == "POST":
		user = request.user
		description = request.POST['description']
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		if phone == "":
			phone = None
		job = request.POST['job']
		if job == "":
			job = None
		company = request.POST['company']
		if company == "":
			company = None
		person = Contact(user=user, phone_number=phone, email=email, name=name, job_title=job, company=company, description=description)
		person.save()
		return HttpResponseRedirect(reverse("contact", args=(person.id, )))

@login_required
def contact(request, contact_id):
	person = Contact.objects.get(pk=contact_id)
	notes = Note.objects.filter(user=request.user, contact=person)
	interactions = Interaction.objects.filter(user=request.user, contact=person)
	return render(request, 'contacts/dashboard/contact.html', {
		"person": person,
		"notes": notes,
		"interactions": interactions
	})


@login_required
def meetings(request):
	return render(request, "contacts/meetings.html")
