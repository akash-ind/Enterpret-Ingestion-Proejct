from django.contrib import admin
from DiscourseIngestion.models import DiscourseFeedbackInfo


# Register your models here.

class DiscourseFeedbackInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(DiscourseFeedbackInfo, DiscourseFeedbackInfoAdmin)
