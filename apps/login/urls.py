from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register', views.register),
	url(r'^login', views.login),
	url(r'^logout', views.logout),
	url(r'^dashboard', views.dashboard),
	url(r'^trip/(?P<trip_id>\d+)/$', views.view),
	url(r'^addtrip$', views.add),
	url(r'^delete_trip/(?P<trip_id>\d+)/$', views.delete_trip),
	url(r'^addtrip_process$', views.add_trip),
	url(r'^join_process/(?P<trip_id>\d+)/$', views.join_process),
	url(r'^cancel_join/(?P<trip_id>\d+)/$', views.cancel_join),
]