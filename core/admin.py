from django.contrib import admin
from .models import Profile
from .models import Patient, Doctor, Appointment, Invoice

admin.site.register(Patient)
admin.site.register(Doctor)
admin.site.register(Appointment)
admin.site.register(Invoice)

admin.site.register(Profile)