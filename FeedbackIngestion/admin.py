from django.contrib import admin
from FeedbackIngestion.models import Feedback, FeedbackMetadata


# Register your models here.

class FeedbackAdmin(admin.ModelAdmin):
    pass


class FeedbackMetadataAdmin(admin.ModelAdmin):
    pass


admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(FeedbackMetadata, FeedbackMetadataAdmin)
