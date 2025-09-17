from django.db import models
from django.contrib.auth.models import AbstractUser

# Extend default User to support roles
class User(AbstractUser):
    ROLE_CHOICES = [
        ("admin", "Admin"),
        ("doctor", "Doctor"),
        ("patient", "Patient"),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="patient")

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="patient_profile")
    dob = models.DateField()
    gender = models.CharField(max_length=10)
    address = models.TextField()
    allergies = models.TextField(blank=True)

    def __str__(self):
        return self.user.username

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={"role": "doctor"})
    scheduled_at = models.DateTimeField()
    status = models.CharField(max_length=20, default="scheduled")

    def __str__(self):
        return f"{self.patient} with {self.doctor} at {self.scheduled_at}"

class Invoice(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default="unpaid")  # unpaid, paid
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.status}"