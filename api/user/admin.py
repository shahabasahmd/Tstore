from django.contrib import admin
from .models import CustomUser
# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')  # Specify the fields you want to display in the list view

admin.site.register(CustomUser, CustomUserAdmin)
