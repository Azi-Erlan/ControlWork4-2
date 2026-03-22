from django.contrib import admin
from .models import Film, Genre, Tag, Comment

admin.site.register(Film)
admin.site.register(Genre)
admin.site.register(Tag)
admin.site.register(Comment)