from django.contrib import admin
from .models import Organizer, Event, Participant, Feedback
from django.utils.html import format_html
from django.urls import reverse

@admin.register(Organizer)
class OrganizerModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'organization_name', 'contact_email']

@admin.register(Event)
class EventModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'organizer', 'name', 'venue', 'date', 'time', 'description', 'organizer_image']

@admin.register(Participant)
class ParticipantModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event']

@admin.register(Feedback)
class FeedbackModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'event', 'participant', 'rating', 'comment']

    def event_info(self, obj):
        link = reverse('admin:your_app_name_event_change', args=[obj.event.pk])
        return format_html('<a href="{}">{}</a>', link, obj.event.name)

    def participant_info(self, obj):
        link = reverse('admin:your_app_name_participant_change', args=[obj.participant.pk])
        return format_html('<a href="{}">{}</a>', link, obj.participant.user.username)
