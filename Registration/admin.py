from django.contrib import admin
from Registration.models import PlayStoreRegistration, TwitterRegistration, DiscourseRegistration, IntercomRegistration


# Register your models here.

class PlayStoreRegistrationAdmin(admin.ModelAdmin):
    pass


class TwitterRegistrationAdmin(admin.ModelAdmin):
    pass


class DiscourseRegistrationAdmin(admin.ModelAdmin):
    pass


class IntercomRegistrationAdmin(admin.ModelAdmin):
    pass


admin.site.register(PlayStoreRegistration, PlayStoreRegistrationAdmin)
admin.site.register(TwitterRegistration, TwitterRegistrationAdmin)
admin.site.register(DiscourseRegistration, DiscourseRegistrationAdmin)
admin.site.register(IntercomRegistration, IntercomRegistrationAdmin)
