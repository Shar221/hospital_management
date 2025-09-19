from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from .models import Appointment, Patient, Doctor
from .forms import AppointmentForm

@login_required
def dashboard(request):
    role = request.user.profile.role

    if role == "admin":
        patients = Patient.objects.all()
        doctors = Doctor.objects.all()
        appointments = Appointment.objects.all()
        context = {
            "role": role,
            "patients": patients,
            "doctors": doctors,
            "appointments": appointments,
        }
        return render(request, "core/dashboard.html", context)

    elif role == "doctor":
        doctor = Doctor.objects.filter(email=request.user.email).first()
        appointments = Appointment.objects.filter(doctor=doctor) if doctor else []
        context = {
            "role": role,
            "doctor": doctor,
            "appointments": appointments,
        }
        return render(request, "core/dashboard.html", context)

    elif role == "patient":
        patient = Patient.objects.filter(email=request.user.email).first()
        appointments = Appointment.objects.filter(patient=patient) if patient else []
        context = {
            "role": role,
            "patient": patient,
            "appointments": appointments,
        }
        return render(request, "core/dashboard.html", context)

    else:
        return render(request, "core/dashboard.html", {"role": "unknown"})
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("dashboard")
    else:
        form = AuthenticationForm()
    return render(request, "core/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("login")

@login_required
def dashboard(request):
    return render(request, "core/dashboard.html")

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        role = request.POST.get("role")  # get selected role
        if form.is_valid():
            user = form.save()
            # Assign role to profile
            user.profile.role = role
            user.profile.save()
            login(request, user)  # log in new user immediately
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})


@login_required
def book_appointment(request):
    if request.user.profile.role != "patient":
        return redirect("dashboard")  # only patients can book

    patient = Patient.objects.filter(email=request.user.email).first()
    if not patient:
        return redirect("dashboard")  # safety check

    if request.method == "POST":
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = patient  # link appointment to logged-in patient
            appointment.save()
            return redirect("dashboard")
    else:
        form = AppointmentForm()

    return render(request, "core/book_appointment.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        role = request.POST.get("role")  
        if form.is_valid():
            user = form.save()
            profile, created = Profile.objects.get_or_create(user=user)
            profile.role = role
            profile.save()
            login(request, user)  
            return redirect("dashboard")
    else:
        form = UserCreationForm()
    return render(request, "core/signup.html", {"form": form})

@login_required
def dashboard(request):
    if request.user.is_superuser:
        role = "admin"
    else:
        role = request.user.profile.role   

@login_required
def dashboard(request):
    # Superuser goes to admin site
    if request.user.is_superuser:
        return redirect("/admin/")

    # Make sure profile exists
    profile = getattr(request.user, "profile", None)
    if not profile:
        return redirect("/admin/")  

    role = profile.role

    if role == "doctor":
        return render(request, "core/doctor_dashboard.html")
    elif role == "patient":
        return render(request, "core/patient_dashboard.html")
    elif role == "admin":
        return redirect("/admin/") 

   
    return render(request, "core/dashboard.html", {"message": "Unknown role"})        