from django.contrib import admin

# Register your models here.

from EaganJones.models import Companies
from home.models import Contact, Comment


class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject','create_at','read')
    list_filter = ('read', 'create_at')

admin.site.site_title = 'Dara Food Admin Panel'
admin.site.site_header = 'Dara Food Admin Panel'
admin.site.index_title = 'Dara Food Admin Panel Home'



class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'product', 'subject', 'message', 'rating', 'status', 'create_at']
    list_filter = ['status', 'create_at']
    readonly_fields = ['product', 'user', 'subject', 'message', 'rating']
    list_display_links = ['user', 'subject','product']
    list_editable = ['status']

admin.site.register(Contact, ContactAdmin)
admin.site.register(Comment, CommentAdmin)
