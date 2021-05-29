from django.contrib import admin

from .models import Request, Comment

admin.site.register(Request)
admin.site.register(Comment)
