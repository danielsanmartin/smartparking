from django.contrib import admin
from .models import OCRCamera, OCRCameraEvent, OCRCameraAlert, Space, SpaceEvent, SpaceAlert, Unity, Visitor, Restriction


class SpaceAdmin(admin.ModelAdmin):
    list_display = ['code', 'sector','type', 'status','unity']
    search_fields = ['code']

class SpaceEventAdmin(admin.ModelAdmin):
    list_display = ['event_date', 'space','type']

class SpaceAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_date', 'space', 'description']

class OCRCameraAdmin(admin.ModelAdmin):
    list_display = ['code', 'unity']
    search_fields = ['code']

class OCRCameraAlertAdmin(admin.ModelAdmin):
    list_display = ['alert_date','plate', 'description']
    search_fields = ['plate']

class OCRCameraEventAdmin(admin.ModelAdmin):
    list_display = ['event_date','plate', 'type', 'cameraOCR']
    search_fields = ['plate']

class UnityAdmin(admin.ModelAdmin):
    list_display = ['name', 'location']
    search_fields = ['code']    

class VisitorAdmin(admin.ModelAdmin):
    list_display = ['plate', 'status', 'enter_date', 'exit_date']
    search_fields = ['plate']

class RestrictionAdmin(admin.ModelAdmin):
    list_display = ['plate', 'expiration_date', 'unity']
    search_fields = ['plate']
    
admin.site.register(OCRCamera, OCRCameraAdmin)
admin.site.register(OCRCameraAlert, OCRCameraAlertAdmin)


admin.site.register(OCRCameraEvent, OCRCameraEventAdmin)
admin.site.register(Space, SpaceAdmin)
admin.site.register(SpaceEvent, SpaceEventAdmin)
admin.site.register(SpaceAlert, SpaceAlertAdmin)
admin.site.register(Unity, UnityAdmin)
admin.site.register(Visitor, VisitorAdmin)

admin.site.register(Restriction, RestrictionAdmin)