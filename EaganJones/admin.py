from django.contrib import admin

# Register your models here.
from django.contrib.postgres import fields
from django_json_widget.widgets import JSONEditorWidget

from EaganJones.models import Companies


@admin.register(Companies)
class CompaniesAdmin(admin.ModelAdmin):
    list_display = ['companyname', 'cik', 'primarysymbol' ]
    list_filter = ['companyname', 'cik', 'primarysymbol']
    search_fields = ('companyname', 'cik', 'primarysymbol')
    list_display_links = ['primarysymbol', 'companyname', ]
    formfield_overrides = {
            fields.JSONField: {'widget': JSONEditorWidget},
    }

