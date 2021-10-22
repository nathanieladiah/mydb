# mydb
## A personal db for your life

#### [Video Demo](https://youtu.be/PitVpRMRot8)


#### Description:
I have created a web application using django Python, and JavaScript.

The software allows you to add contacts, and keep track of your interactions with them.

Currently you can create a user, and then create contacts, and record interactions with them such as calls, activities, reminders and events. 

Then you can see each contact on an individual page. JavaScript functions allow you to dynamically edit, or delete these interactions.

When fully realized, there will be notifications on the dashboard page that will notify you if you haven't contacted/ interacted with a person within a set timeframe. But for now that feature is not completed.

### Build Log

#### 25th September 2021


* Create new django project and app

* Create models for the app
	* installed django-phonenumber-field

---

#### 17th October 2021

* Each contact should have a page where their info is stored:
	* Name
	* Connections - people in common?
	* info - miscellaneous information about them
	* email
	* contact numbers
	* job and company.

* Use a different template for the dashboard
TODO: When a page loads remove collapsed from class list and add it to all others (check if they have it first) in the side nav

* Should it be a single page app with javascript to load the different sections?

#### 18th October 2021

* Contactlist and contact page design complete


#### 19th October 2021

* Create dashboard template
* The upcoming events list should list all the events for upcoming days in the current month
* Alerts should list off people that haven't been contacted a long time, also birthdays/anniversaries