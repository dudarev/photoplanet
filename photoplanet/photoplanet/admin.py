from django.contrib import admin

from feedback.models import Feedback


class FeedbackAdmin(admin.ModelAdmin):
    readonly_fields = ['created_at', ]
    pass


admin.site.register(Feedback, FeedbackAdmin)
