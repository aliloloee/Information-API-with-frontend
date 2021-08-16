from django.contrib import admin
from .models import User, DefinedPeople


@admin.register(User)
class UserAdmin(admin.ModelAdmin) :
    list_display = ('username', 'id', 'user_type', 'is_active', 'is_admin', 'is_superuser', )
    list_filter = ('user_type',)

admin.site.register(DefinedPeople)