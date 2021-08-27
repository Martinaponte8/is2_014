from django.conf.urls import url
from django.urls import path
#from django import forms
#from usuarios import views
#
from . import views
urlpatterns = [
    url(r'^$', views.UserListView.as_view(), name='user_list'), url(r'^create/$', views.CreateUserView.as_view(), name='create_user'), path(route='update_user/<int:pk>/', view=views.UpdateUserView.as_view(), name='update_user'),
]
