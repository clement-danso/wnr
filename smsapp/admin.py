from django.contrib import admin
from smsapp.models import *
from smsapp.resources import *
from import_export.admin import ImportExportModelAdmin


class RecordsAdmin(ImportExportModelAdmin):
	exclude = ('status','date_created', 'date_updated')
	list_display = ('EmpNumber', 'FirstName', 'LastName', 'OfficialEmail', 'Mobile', 'category', 'grade', 'bmc', 'status', 'date_created')
	resource_class=recordsResource   

# Register your models here.
admin.site.register(unit)
admin.site.register(bmc)
admin.site.register(subdistrict)
admin.site.register(district)
admin.site.register(region)
admin.site.register(grade)
#admin.site.register(broadcastmessage)
admin.site.register(group)
admin.site.register(records, RecordsAdmin)
admin.site.register(delivery)
admin.site.register(category)


