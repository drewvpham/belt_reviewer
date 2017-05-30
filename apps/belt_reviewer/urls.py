from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^$', views.index, name='landing'),
    url(r'^register$', views.register, name='register'),
    url(r'^login$', views.login, name='login'),
    url(r'^books$', views.books, name='books'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^book/add$', views.add_book, name='add_book'),
    url(r'^book/add$', views.add_book, name='add_book'),
    url(r"^users/(?P<id>\d+)", views.users),
]
