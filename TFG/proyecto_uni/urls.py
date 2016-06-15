# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout',views.user_logout, name='logout'),
    url(r'^signup', views.user_signup, name='signup'),
    url(r'^about', views.about, name='about'),
    url(r'^contact', views.contact, name='contact'),
    url(r'^studies.*', views.studies, name='studies'),
    url(r'^details.*', views.details, name='details'),
    url(r'^search.*', views.search, name='search'),
    url(r'^compare', views.choose_studies, name='compare'),
    url(r'^comment/post.*', views.comment, name='comment'),
    url(r'^comment/edit.*', views.edit_comment, name='edit'),
    url(r'^comment/delete.*', views.delete_comment, name='delete'),  
    url(r'^comment/confirm.*', views.delete_confirm, name='confirm'), 
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]