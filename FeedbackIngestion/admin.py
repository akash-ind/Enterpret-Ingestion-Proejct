from django.contrib import admin
from FeedbackIngestion.models import Feedback, FeedbackMetadata, DiscourseFeedbackInfo


# Register your models here.

class FeedbackAdmin(admin.ModelAdmin):
    pass


class FeedbackMetadataAdmin(admin.ModelAdmin):
    pass


class DiscourseFeedbackInfoAdmin(admin.ModelAdmin):
    pass


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackMetadata, FeedbackMetadataAdmin)
admin.site.register(DiscourseFeedbackInfo, DiscourseFeedbackInfoAdmin)
