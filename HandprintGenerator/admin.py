from django.contrib import admin

from .models import *

class UserAdmin(admin.ModelAdmin):
    pass
admin.site.register(User, UserAdmin)

#class ActionItemAdmin(admin.ModelAdmin)
#    pass
#admin.site.register(ActionItem, ActionItemAdmin)