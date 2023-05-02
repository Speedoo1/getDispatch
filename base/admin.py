from django.contrib import admin

# Register your models here.
from base.models import user, proposal, ride


class proposalAdmin(admin.ModelAdmin):
    list_display = ('goodsName', 'id', 'deliver', 'accepted')
    search_fields = ('goodsName', 'id', 'deliver', 'accepted')

    def get_form(self, request, obj=None, **kwargs):
        self.exclude = ['deliveryPassword']
        if request.user.is_superuser:
            self.exclude[0] = ''

        return super(proposalAdmin, self).get_form(request, obj, **kwargs)


class rideAdmin(admin.ModelAdmin):
    list_display = ('username', 'rideName', 'phoneNumber', 'rideType', 'verified')
    search_fields = ('username', 'rideName', 'phoneNumber', 'rideType', 'verified')


admin.site.register(user)
admin.site.register(proposal, proposalAdmin)
admin.site.register(ride, rideAdmin)
