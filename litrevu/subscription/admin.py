from django.contrib import admin
from .models import UserFollows

class UserFollowsAdmin(admin.ModelAdmin):
    pass

admin.site.register(UserFollows, UserFollowsAdmin)
