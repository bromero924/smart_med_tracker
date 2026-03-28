from django.contrib import admin
from .models import Medication, TreatmentPlan, DoseLog, DeviceEvent

admin.site.register(Medication)
admin.site.register(TreatmentPlan)
admin.site.register(DoseLog)
admin.site.register(DeviceEvent)
