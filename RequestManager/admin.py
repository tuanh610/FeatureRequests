from django.contrib import admin
from .models import adminUser, ClientDetail, Request
# Register your models here.
admin.site.register(adminUser)
admin.site.register(ClientDetail)
admin.site.register(Request)
