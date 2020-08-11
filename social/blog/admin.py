from django.contrib import admin
from .models import Post      # import the post model from models.py
admin.site.register(Post)