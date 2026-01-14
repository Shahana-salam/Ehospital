from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from doctorapp.models import Doctor
from facility.models import Department
from patientapp.models import Patient, Appointment


def home(request):
    return redirect('login')


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # Role-based redirect
            if user.role == 'ADMIN':
                return redirect('admin_dashboard')
            elif user.role == 'DOCTOR':
                return redirect('doctor_dashboard')
            else:
                return redirect('patient_dashboard')
        else:
            messages.error(request, 'Invalid username or password')

    return render(request, 'accounts/login.html')








def admin_dashboard(request):
    context = {
        'total_patients': Patient.objects.count(),
        'total_doctors': Doctor.objects.count(),
        'total_departments': Department.objects.count(),
        'total_appointments': Appointment.objects.count(),

        'new_patients': Patient.objects.order_by('-created_at')[:5]

    }
    return render(request, 'admin/dashboard.html', context)



