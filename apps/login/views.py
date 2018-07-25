from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
	return render(request, 'login/index.html')

def register(request):
	# add function to search database if 
	errors = User.objects.registration_validator(request.POST)
	if len(errors):
		for key, value in errors.items():
			messages.error(request, value)
		print(errors)
		return redirect('/')
	else:
		User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()))
		user = User.objects.filter(email = request.POST['email'])
		request.session['user_id'] = user.values()[0]['id']
		request.session['user_first_name'] = user.values()[0]['first_name']
		request.session['user_last_name'] = user.values()[0]['last_name']
		request.session['user_email'] = user.values()[0]['email']
		return redirect('/dashboard')

def login(request):
	if request.method == 'POST':
		errors = User.objects.login_validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			print(errors)
			return redirect('/')
		else:
			user = User.objects.filter(email = request.POST['email'])
			request.session['user_id'] = user.values()[0]['id']
			request.session['user_first_name'] = user.values()[0]['first_name']
			request.session['user_last_name'] = user.values()[0]['last_name']
			request.session['user_email'] = user.values()[0]['email']
			print(request.session.values())
			return redirect('/dashboard')

def logout(request):
	request.session.flush()
	return redirect('/')

def dashboard(request):
	if 'user_id' in request.session:
		context = {
		'trips' : Trip.objects.all(),
		'users' : User.objects.all(),
		'this_user' : User.objects.get(id=request.session['user_id']),
		}
		return render(request, 'login/dashboard.html', context)
	else:
		return redirect('/')

def add(request):
	if 'user_id' in request.session:
		return render(request, 'login/add.html')
	else:
		return redirect('/')

def add_trip(request):
	if 'user_id' in request.session:
		errors = Trip.objects.validator(request.POST)
		if len(errors):
			for key, value in errors.items():
				messages.error(request, value)
			print(errors)
			return redirect('/addtrip')
		else:
			this_trip = Trip(name=request.POST['name'], plan=request.POST['plan'], start=request.POST['start'], end=request.POST['end'], joined=User.objects.get(id=request.session['user_id']), uploaded_by=User.objects.get(id=request.session['user_id']))
			this_trip.save()
			this_user = User.objects.get(id=request.session['user_id'])
			this_trip = Trip.objects.get(id=this_trip.id)
			this_trip.join.add(this_user)
			return redirect('/dashboard')
	else:
		return redirect('/')

def view(request, trip_id):
	if 'user_id' in request.session:
		context = {
		'trips' : Trip.objects.get(id=trip_id),
		'this_user' : User.objects.get(id=request.session['user_id']),
		}
		return render(request, 'login/view.html', context)
	else:
		return redirect('/')

def delete_trip(request, trip_id):
	q = Trip.objects.get(id=trip_id)
	q.delete()
	return redirect('/dashboard')

def join_process(request, trip_id):
	if 'user_id' in request.session:
		this_user = User.objects.get(id=request.session['user_id'])
		this_trip = Trip.objects.get(id=trip_id)
		this_trip.join.add(this_user)
		this_trip.joined_id = this_user
		this_trip.save()
		return redirect('/dashboard')
	else:
		return redirect('/')

def cancel_join(request, trip_id):
	if 'user_id' in request.session:
		other_user = User.objects.get(id=0)
		this_user = User.objects.get(id=request.session['user_id'])
		this_trip = Trip.objects.get(id=trip_id)
		this_trip.join.remove(this_user)
		this_trip.joined_id = other_user
		this_trip.save()
		return redirect('/dashboard')
	else:
		return redirect('/')