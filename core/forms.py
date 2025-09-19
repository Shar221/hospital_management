from django import forms
from .models import Appointment

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["doctor", "date", "reason"]
        widgets = {
            "date": forms.DateTimeInput(attrs={"type": "datetime-local"})
        }