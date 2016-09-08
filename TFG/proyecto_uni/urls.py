# -*- coding: utf-8 -*-

# Copyright 2016 Alvaro Feal 
# This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.

#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.

#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.


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
    url(r'^compare', views.choose_campus, name='compare'),
    url(r'^show_compare.*', views.choose_titulacion, name='compare'),
    url(r'^comment/post.*', views.comment, name='comment'),
    url(r'^comment/edit.*', views.edit_comment, name='edit'),
    url(r'^comment/delete.*', views.delete_comment, name='delete'),  
    url(r'^comment/confirm.*', views.delete_confirm, name='confirm'), 
    url(r'^ratings/', include('star_ratings.urls', namespace='ratings', app_name='ratings')),
]