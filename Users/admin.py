from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'created_at', 'updated_at')
    search_fields = ('email',)
    ordering = ('-created_at',)