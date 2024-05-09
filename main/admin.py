from django.contrib import admin
from .models import CustomUser, Post, MethodologicalResource, Reaction


admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(MethodologicalResource)
admin.site.register(Reaction)
