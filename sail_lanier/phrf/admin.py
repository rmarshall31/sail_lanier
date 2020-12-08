from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Boat, Cert, CertRequest, Profile, TransferRequest

admin.site.site_header = 'Sail Lanier Admin'
admin.site.register(CertRequest)
admin.site.register(TransferRequest)


@admin.register(Boat)
class BoatAdmin(admin.ModelAdmin):
    list_display = ('boat_name', 'sail_number', 'boat_type', 'owner_name')
    search_fields = ('boat_name', 'boat_type', 'owner__first_name', 'owner__last_name')


@admin.register(Cert)
class CertAdmin(admin.ModelAdmin):
    list_display = ('boat_name', 'boat_type', 'owner_name', 'base_rating', 'adjusted_rating', 'expiration_date')
    search_fields = ('boat__boat_name', 'boat__boat_type', 'boat__owner__last_name')


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
