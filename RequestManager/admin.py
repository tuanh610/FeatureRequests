""" Register models for built-in admin pages
You can choose what models can show up in the admin page
Tou can also choose which fields that modifiable and which to shows

This project will just register all the important models
But if further change is needed, it can be modified further.
Reference: https://docs.djangoproject.com/en/3.0/intro/tutorial07/
"""
from django.contrib import admin
from .models import adminUser, ClientDetail, Request

# Register 3 models:
# 1.adminUser (to be used to create log in later
# 2.clientDetail: to store the client name to display in request submission/edit
# 3.Request: to store information about the request itself
admin.site.register(adminUser)
admin.site.register(ClientDetail)
admin.site.register(Request)
