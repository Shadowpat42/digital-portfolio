from django.contrib import admin
from .models import CustomUser, Post, MethodologicalResource, Reaction, Media


admin.site.register(CustomUser)
admin.site.register(Post)
admin.site.register(MethodologicalResource)
admin.site.register(Reaction)
admin.site.register(Media)
