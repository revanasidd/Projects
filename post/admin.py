from django.contrib import admin
from post.models import *
from django.contrib.auth.models import User
# Register your models here.
class UserAdmin(admin.ModelAdmin):
	list_display = ["id","username","first_name","last_name"]
	search_fields = ["id","username","first_name","last_name"]
admin.site.unregister(User)
admin.site.register(User,UserAdmin)
admin.site.register(Post)
admin.site.register(Followed)