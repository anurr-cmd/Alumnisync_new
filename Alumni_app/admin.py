from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Event, Job, Announcement
from .models import Feedback

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "roll_no",
        "department",
        "passout_year",
        "company",
        "location",
        "profile_image_preview",

    )
    list_filter = ("role", "department", "passout_year")
    search_fields = ("user__username", "roll_no", "company")
    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.profile_image.url
            )
        return "No Image"

    profile_image_preview.short_description = "Profile Image"

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "date",
        "created_by",
        "is_approved",
        "is_rejected",
    )
    list_filter = ("date", "is_approved", "is_rejected")
    search_fields = ("title", "description")


@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "company",
        "posted_by",
        "posted_on",
    )
    list_filter = ("company", "posted_on")
    search_fields = ("title", "company")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "posted_on",
    )
    search_fields = ("title", "message")

admin.site.register(Feedback)