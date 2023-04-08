from django.contrib import admin

# Register your models here.
from base.models import user, proposal, ride

admin.site.register(user)
admin.site.register(proposal)
admin.site.register(ride)