import json
from django.http.response import JsonResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from datetime import date
import datetime

from .models import Contact, Interaction, User, Note, Event
from .forms import ContactForm

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
	# print(date.today())	
	# today = date.today()
	# print(datetime.datetime.now())
	# Only get events for dates that haven't gone already
	events = Event.objects.filter(user=request.user, date__gte=date.today()).order_by('date').all()

	# Get a list of all contacts for this user
	contacts = Contact.objects.filter(user=request.user).all()

	alerts = []
	
	# For each contact, get the latest interaction that they had with the user
	for contact in contacts:
		last_interaction = Interaction.objects.filter(contact=contact).order_by('-date').first()
		print(last_interaction)
		if not last_interaction: #or last_interaction.date
			alert = f"Interaction with {contact.name} due"
			alerts.append(alert)

	return render(request, "contacts/dashboard/dashboard.html", {
		'events': events,
		'alerts': alerts
	}) 

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

# Get a specific contact from a user
@login_required
def contact_info(request, contact_id):
	# Query for specific contact
	try:
		contact = Contact.objects.get(pk=contact_id)
	except Contact.DoesNotExist:
		return JsonResponse({"error": "Contact not found."}, status=404)

	# Return contact details
	if request.method == "GET":
		return JsonResponse(contact.serialize())
	
	else:
		return JsonResponse({"error": "GET request required"}, status=400)


# Edit contact info
@login_required
def edit_about(request, contact_id):

	# Make sure it's a post request
	if request.method != 'POST':
		return JsonResponse({"error": "POST request is required"}, status=400)

	data = json.loads(request.body)

	contact = Contact.objects.get(pk=contact_id)
	contact.description = data.get("description")
	contact.save()
	return JsonResponse({"message": "Post edited successfully."}, status=201)

# Add a note for a user
@login_required
def add_note(request, contact_id):
	if request.method == 'POST':
		body = request.POST['note']
		contact = Contact.objects.get(pk=contact_id)
		note = Note(body=body, user=request.user, contact=contact)
		note.save()
		return HttpResponseRedirect(reverse("contact", args=(contact_id, )))

# Get a specific note:
@login_required
def note(request, note_id):

	try: 
		note = Note.objects.get(pk=note_id)
	except Note.DoesNotExist:
		return JsonResponse({"error": "Note not found."}, status=404)

	# Return note contents
	if request.method == 'GET':
		return JsonResponse(note.serialize())
	else:
		return JsonResponse({"error": "GET request required."}, status=400)


# Edit a specific post
@login_required
def edit_note(request, note_id):

	if request.method != 'POST':
		return JsonResponse({"error": "POST request required."}, status=403)

	data = json.loads(request.body)

	note = Note.objects.get(pk=note_id)
	note.body = data.get('body')
	note.save()
	return JsonResponse({"message": "Post edited successfully."}, status=201)

@login_required
def delete_note(request, note_id):
	if request.method != 'POST':
		return JsonResponse({"error": "POST request required."}, status=403)

	note = Note.objects.get(pk=note_id)
	note.delete()
	return JsonResponse({"message": "Post edited successfully."}, status= 201)

@login_required
def add_interaction(request, contact_id):
	if request.method == 'POST':
		body = request.POST['body']
		type = request.POST['type']
		date = request.POST['date']
		user = request.user
		contact = Contact.objects.get(pk=contact_id)
		interaction = Interaction(contact=contact, body=body, user=user, type=type, date=date)
		interaction.save()
		return HttpResponseRedirect(reverse("contact", args=(contact_id, )))


# Get a specific interaction:
@login_required
def interaction(request, interaction_id):

	try: 
		interaction = Interaction.objects.get(pk=interaction_id)
	except Interaction.DoesNotExist:
		return JsonResponse({"error": "Interaction not found."}, status=404)

	# Return interaction contents
	if request.method == 'GET':
		return JsonResponse(interaction.serialize())
	else:
		return JsonResponse({"error": "GET request required."}, status=400)

# # Edit a specific Interaction
@login_required
def edit_interaction(request, interaction_id):

	if request.method != 'POST':
		return JsonResponse({"error": "POST request required."}, status=403)

	data = json.loads(request.body)

	interaction = Interaction.objects.get(pk=interaction_id)
	interaction.body = data.get('body')
	interaction.save()
	return JsonResponse({"message": "Interaction edited successfully."}, status=201)


@login_required
def delete_interaction(request, interaction_id):
	if request.method != 'POST':
		return JsonResponse({"error": "POST request required."}, status=403)

	interaction = Interaction.objects.get(pk=interaction_id)
	interaction.delete()
	return JsonResponse({"message": "Interaction deleted."}, status= 201)

@login_required
def edit_contact(request, contact_id):
	if request.method == 'POST':
		contact = Contact.objects.get(pk=contact_id)

		contact.name = request.POST['fullName']
		contact.description = request.POST['about']
		contact.company = request.POST['company']
		contact.job = request.POST['job']
		contact.country = request.POST['country']
		contact.address = request.POST['address']
		contact.phone = request.POST['phone']
		contact.email = request.POST['email']
		contact.twitter = request.POST['twitter']
		contact.facebook = request.POST['facebook']
		contact.instagram = request.POST['instagram']
		contact.linkedin = request.POST['linkedin']
		contact.save()

		return HttpResponseRedirect(reverse("contact", args=(contact_id, )))

@login_required
def contact_pic(request, contact_id):
	if request.method == "POST":
		contact = Contact.objects.get(pk=contact_id)
		form = ContactForm(request.POST, request.FILES, instance=contact)
		if form.is_valid():
			form.save()
		return HttpResponseRedirect(reverse("contact", args=(contact_id, )))
	
	form = ContactForm()
	contact = Contact.objects.get(pk=contact_id)
	return render(request, "contacts/dashboard/cpicupload.html", {
		"contact": contact,
		"form": form
	})