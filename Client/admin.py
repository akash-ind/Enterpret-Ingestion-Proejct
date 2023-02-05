from django.contrib import admin
from Client.models import Client, Application
# Register your models here.

class ClientAdmin(admin.ModelAdmin):
    pass

class ApplicationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Client, ClientAdmin)
admin.site.register(Application, ApplicationAdmin)