from __future__ import unicode_literals
from django.db import models
import datetime
import re, bcrypt

# Create your models here.
class UserManager(models.Manager):
	def registration_validator(self, postData):
		EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
		errors = {}
		if len(postData['first_name']) < 2:
			errors['first_name'] = 'First name should be at least 2 characters'
		if len(postData['last_name']) < 2:
			errors['last_name'] = 'Last name should be at least 2 characters'
		if len(postData['email']) < 1:
			errors['email'] = 'Please fill out email'
		elif not EMAIL_REGEX.match(postData['email']):
			errors['email_valid'] = 'Email is not valid!'
		if len(User.objects.filter(email = postData['email'])) > 0:
			errors['existing_email'] = 'Email is already in use.'
		if len(postData['password']) < 8:
			errors['password_length'] = 'Password must be at least 8 characters'
		if postData['password'] != postData['password_confirm']:
			errors['password_confirm'] = 'Passwords do not match'
		return errors

	def login_validator(self, postData):
		errors = {}
		user = User.objects.filter(email = postData['email'])
		if len(user) < 1:
			errors['unknown'] = 'Invalid credentials'
		else:
			if bcrypt.checkpw(postData['password'].encode(), user.values()[0]['password'].encode()) == False:
				errors['badpw'] = 'Wrong password'
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	objects = UserManager()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

class TripManager(models.Manager):
	def validator(self, postData):
		errors = {}
		if len(postData['name']) < 1:
			errors['name'] = 'Name should not be empty'
		if len(postData['start']) < 1:
			errors['start'] = 'Date should not be empty'
		if len(postData['end']) < 1:
			errors['end'] = 'Date should not be empty'
		if len(postData['plan']) < 1:
			errors['plan'] = 'Plan should not be empty'
		if postData['start'] < postData['end']:
			errors['matching_date'] = 'Start Date should not be before the end date'
		# if postData['start'] < datetime.datetime.today():
		# 	errors['matching_date'] = 'Start date should be future-dated'
		return errors

class Trip(models.Model):
	name = models.CharField(max_length=255)
	start = models.DateField()
	end = models.DateField()
	plan = models.CharField(max_length=255)
	objects = TripManager()
	uploaded_by = models.ForeignKey(User, related_name="uploaded_by")
	join = models.ManyToManyField(User, related_name="join")
	joined = models.ForeignKey(User, related_name="joined")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)