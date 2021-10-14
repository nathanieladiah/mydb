from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login", views.login_view, name="login"),
	path("logout", views.logout_view, name="logout"),
	path("register", views.register, name="register"),
	path("dashboard", views.dashboard, name="dashboard"),
	path("contacts", views.contacts, name="contacts"),
	path("meetings", views.meetings, name="meetings"),
	path("contact/<int:contact_id>", views.contact, name="contact")
]