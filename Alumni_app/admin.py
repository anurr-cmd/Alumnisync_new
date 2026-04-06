from django.contrib import admin
from django.utils.html import format_html
from .models import Profile, Event, Announcement
from .models import Feedback
from django.contrib.auth.models import Group

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "role",
        "roll_no",
        "department",
        "join_year",
        "passout_year",
        "designation",
        "current_job",
        "company",
        "location",
        "phone",
        "profile_image_preview",
        "proof_id_link",
        "company_id_image_link",
        "appointment_order_link",
        "linkedin_profile_link",
        "google_scholar_link",
    )

    list_filter = (
        "role",
        "department",
        "join_year",
        "passout_year",
        "designation",
        "company",
        "location",
    )

    search_fields = (
        "user__username",
        "roll_no",
        "email",
        "department",
        "designation",
        "current_job",
        "company",
        "location",
        "phone",
        "alternate_phone",
        "linkedin_profile",
        "google_scholar",
    )

    readonly_fields = (
        "profile_image_preview",
        "proof_id_link",
        "company_id_image_link",
        "appointment_order_link",
        "linkedin_profile_link",
        "google_scholar_link",
    )

    def profile_image_preview(self, obj):
        if obj.profile_image:
            return format_html(
                '<img src="{}" width="50" height="50" style="border-radius:50%;" />',
                obj.profile_image.url
            )
        return "No Image"
    profile_image_preview.short_description = "Profile Image"

    def proof_id_link(self, obj):
        if obj.proof_id:
            return format_html('<a href="{}" target="_blank">View Proof ID</a>', obj.proof_id.url)
        return "No File"
    proof_id_link.short_description = "Proof ID"

    def company_id_image_link(self, obj):
        if obj.company_id_image:
            return format_html('<a href="{}" target="_blank">View Company ID</a>', obj.company_id_image.url)
        return "No File"
    company_id_image_link.short_description = "Company ID Image"

    def appointment_order_link(self, obj):
        if obj.appointment_order:
            return format_html('<a href="{}" target="_blank">View Appointment Order</a>', obj.appointment_order.url)
        return "No File"
    appointment_order_link.short_description = "Appointment Order"

    def linkedin_profile_link(self, obj):
        if obj.linkedin_profile:
            return format_html('<a href="{}" target="_blank">LinkedIn</a>', obj.linkedin_profile)
        return "No Link"
    linkedin_profile_link.short_description = "LinkedIn"

    def google_scholar_link(self, obj):
        if obj.google_scholar:
            return format_html('<a href="{}" target="_blank">Scholar</a>', obj.google_scholar)
        return "No Link"
    google_scholar_link.short_description = "Google Scholar"

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


# @admin.register(Job)
# class JobAdmin(admin.ModelAdmin):
#     list_display = (
#         "title",
#         "company",
#         "posted_by",
#         "posted_on",
#     )
#     list_filter = ("company", "posted_on")
#     search_fields = ("title", "company")


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "posted_on",
    )
    search_fields = ("title", "message")

# admin.site.register(Feedback)

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "created_at")
    search_fields = ("user__username", "message")
    list_filter = ("created_at",)

admin.site.unregister(Group)