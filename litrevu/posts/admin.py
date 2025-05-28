from django.contrib import admin
from .models import Ticket, Review


class TicketAdmin(admin.ModelAdmin):
    pass


class ReviewAdmin(admin.ModelAdmin):
    pass


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Review, ReviewAdmin)
