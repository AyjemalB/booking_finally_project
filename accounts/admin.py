from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User
from listings.models import Listing


class ListingInline(admin.TabularInline):
    model = Listing
    fk_name = 'owner'
    extra = 0
    readonly_fields = ('title', 'description')
    can_delete = False

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_editable = ('is_active',) #Удаление и блокировка пользователей

    fieldsets = UserAdmin.fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role Info', {'fields': ('role',)}),
    )
    inlines = [ListingInline]

admin.site.register(User, CustomUserAdmin)
