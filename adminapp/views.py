from django.contrib import admin, messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from accounts.forms import DoctorForm
from accounts.models import User
from adminapp.forms import DepartmentForm, LocationForm
from doctorapp.models import Doctor
from facility.models import Department, Location
from patientapp.models import Patient, Appointment, Billing


# Create your views here.



def is_admin(user):
    return user.is_authenticated and user.role == 'ADMIN'

# Manage doctors
@login_required
@user_passes_test(is_admin)
def manage_doctors(request):
    doctors = Doctor.objects.all()
    return render(request, 'admin/manage_doctor.html', {'doctors': doctors})



@login_required
@user_passes_test(is_admin)

def add_doctor(request):
    if request.method == 'POST':
        form = DoctorForm(request.POST)
        if form.is_valid():

            # 1️⃣ Create User
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role='DOCTOR',
                is_active=True,
                is_staff=True
            )

            # 2️⃣ Create Doctor (without saving)
            doctor = form.save(commit=False)
            doctor.user = user
            doctor.save()

            messages.success(request, "Doctor added successfully")
            return redirect('manage_doctors')
    else:
        form = DoctorForm()

    return render(request, 'admin/doctor_form.html', {'form': form})




def edit_doctor(request, pk):
    doctor = Doctor.objects.get(pk=pk)
    user = doctor.user

    if request.method == 'POST':
        form = DoctorForm(request.POST, instance=doctor)

        if form.is_valid():
            user.username = form.cleaned_data['username']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']

            password = form.cleaned_data.get('password')
            if password:
                user.set_password(password)

            user.save()
            form.save()

            return redirect('manage_doctors')

    else:
        form = DoctorForm(
            instance=doctor,
            initial={
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
            }
        )

    return render(request, 'admin/doctor_form.html', {'form': form})



@login_required

@user_passes_test(is_admin)
def delete_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.user.delete()  # deletes doctor and linked user
        return redirect('manage_doctors')
    return render(request, 'admin/doctor_confirm_delete.html', {'doctor': doctor})



@login_required
@user_passes_test(is_admin)
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_dashboard')
    else:
        form = DepartmentForm()
    return render(request, 'admin/add_department.html', {'form': form})


def edit_department(request, id):
    department = get_object_or_404(Department, id=id)
    form = DepartmentForm(request.POST or None, instance=department)
    if form.is_valid():
        form.save()
        return redirect('facility_dashboard')
    return render(request, 'admin/edit_form.html', {'form': form, 'title': 'Edit Department'})


def delete_department(request, id):
    department = get_object_or_404(Department, id=id)
    department.delete()
    return redirect('facility_dashboard')


@login_required
@user_passes_test(is_admin)
def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_dashboard')
    else:
        form = LocationForm()
    return render(request, 'admin/add_location.html', {'form': form})


def edit_location(request, id):
    location = get_object_or_404(Location, id=id)
    form = LocationForm(request.POST or None, instance=location)
    if form.is_valid():
        form.save()
        return redirect('facility_dashboard')
    return render(request, 'admin/edit_form.html', {'form': form, 'title': 'Edit Location'})


def delete_location(request, id):
    location = get_object_or_404(Location, id=id)
    location.delete()
    return redirect('facility_dashboard')



@login_required
@user_passes_test(is_admin)
def patients_list(request):
    patients = Patient.objects.all()
    return render(request, 'admin/patient.html', {'patients': patients})



@login_required
@user_passes_test(is_admin)
def toggle_patient_status(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    patient.user.is_active = not patient.user.is_active  # toggle
    patient.user.save()
    return redirect('patients_list')




@login_required
def admin_appointments(request):
    if request.user.role != 'ADMIN':
        return redirect('login')

    appointments = Appointment.objects.all().order_by('-created_at')

    if request.method == 'POST':
        appointment = Appointment.objects.get(id=request.POST.get('appointment_id'))

        action = request.POST.get('action')

        if action == 'confirm':
            appointment.status = 'Confirmed'
        elif action == 'cancel':
            appointment.status = 'Cancelled'
        elif action == 'complete':
            appointment.status = 'Completed'

        appointment.save()
        return redirect('admin_appointments')

    return render(request, 'admin/appointments.html', {
        'appointments': appointments
    })



def add_billing(request):
    if request.method == 'POST':
        Billing.objects.create(
            patient_id=request.POST['patient'],
            appointment_id=request.POST['appointment'],
            description=request.POST['description'],
            amount=request.POST['amount']
        )
        return redirect('admin_billing_list')

    context = {
        'patients': Patient.objects.all(),
        'appointments': Appointment.objects.all()
    }
    return render(request, 'admin/add_billing.html', context)


def admin_billing_list(request):
    billings = Billing.objects.all()
    return render(request, 'admin/billing_list.html', {'billings': billings})



