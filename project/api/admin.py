from django.contrib import admin

from .models import Bill, Client, Organization


admin.site.register(Bill)
admin.site.register(Client)
admin.site.register(Organization)
