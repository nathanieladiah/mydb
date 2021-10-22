from django.urls import path

from . import views

urlpatterns = [
	path("", views.index, name="index"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.logout_view, name="logout"),
	path("register/", views.register, name="register"),
	path("dashboard/", views.dashboard, name="dashboard"),
	path("contacts/", views.contacts, name="contacts"),
	path("contact/<int:contact_id>/", views.contact, name="contact"),
	path("contact/<int:contact_id>/add-note/", views.add_note, name="add_note"),
	path("contact/<int:contact_id>/add-interaction/", views.add_interaction, name="add_interaction"),
	path("add_contact/", views.add_contact, name="add_contact"),
	path("contact/<int:contact_id>/edit", views.edit_contact, name="edit_contact"),
	path("contact/<int:contact_id>/upload", views.contact_pic, name="contact_pic"),

	# API urls
	path("contact/<int:contact_id>/details/", views.contact_info, name="get_contact"),
	path("contact/<int:contact_id>/edit/", views.edit_about, name="edit_about"),
	path("note/<int:note_id>/", views.note, name="note"),
	path("note/<int:note_id>/edit", views.edit_note, name="edit_note"),
	path("note/<int:note_id>/delete", views.delete_note, name="delete_note"),
	path("interaction/<int:interaction_id>/", views.interaction, name="interaction"),
	path("interaction/<int:interaction_id>/edit", views.edit_interaction, name="edit_interaction"),
	path("interaction/<int:interaction_id>/delete", views.delete_interaction, name="delete_interaction"),
	# path("interaction/<int:interaction_id>", views.interaction)
]