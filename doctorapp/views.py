from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect

from doctorapp.models import Doctor
from facility.models import Department
from patientapp.models import Appointment, Patient, MedicalRecord




@login_required
def doctor_dashboard(request):
    if request.user.role != 'DOCTOR':
        return redirect('login')

    doctor = get_object_or_404(Doctor, user=request.user)

    # All appointments for this doctor
    doctor_appointments = Appointment.objects.filter(doctor=doctor).select_related(
        'patient', 'patient__user', 'department', 'location'
    )

    # Unique patients
    doctor_patients = Patient.objects.filter(
        appointment__doctor=doctor
    ).distinct().order_by('-appointment__date')

    # Latest pending appointments
    new_appointments = doctor_appointments.filter(status='Pending').order_by('-date', '-time')[:5]

    context = {
        'total_patients': doctor_patients.count(),
        'total_departments': Department.objects.count(),
        'total_appointments': doctor_appointments.count(),
        'pending_appointments': doctor_appointments.filter(status='Pending').count(),
        'patients': doctor_patients[:5],
        'new_appointments': new_appointments,
    }

    return render(request, 'doctor/dashboard.html', context)



# Patient List
def patient_list(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    patients = Patient.objects.filter(
        appointment__doctor=doctor
    ).distinct()

    return render(
        request,
        'doctor/patient_list.html',
        {'patients': patients}
    )

# Patient Detail
def patient_detail(request, patient_id):
    patient = get_object_or_404(Patient, id=patient_id)
    return render(request, 'doctor/patient_detail.html', {'patient': patient})




def medical_records_list(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    records = MedicalRecord.objects.filter(
        doctor=doctor
    ).select_related('patient', 'patient__user').order_by('-created_at')

    return render(
        request,
        'doctor/medical_records.html',
        {'records': records}
    )


def appointment_list(request):
    doctor = get_object_or_404(Doctor, user=request.user)

    appointments = Appointment.objects.filter(
        doctor=doctor
    ).order_by('date', 'time')

    return render(
        request,
        'doctor/appointments.html',
        {'appointments': appointments}
    )







def appointment_detail(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    medical_record = MedicalRecord.objects.filter(
        patient=appointment.patient,
        doctor=appointment.doctor
    ).first()

    return render(
        request,
        'doctor/appointment_details.html',
        {
            'appointment': appointment,
            'medical_record': medical_record
        }
    )




def add_medical_record_from_appointment(request, appointment_id):
    doctor = get_object_or_404(Doctor, user=request.user)
    appointment = get_object_or_404(
        Appointment,
        id=appointment_id,
        doctor=doctor
    )

    # Prevent duplicate records
    if MedicalRecord.objects.filter(appointment=appointment).exists():
        return redirect('doctor_appointment_detail', appointment_id=appointment.id)

    if request.method == 'POST':
        MedicalRecord.objects.create(
            patient=appointment.patient,
            doctor=doctor,
            appointment=appointment,
            diagnosis=request.POST['diagnosis'],
            prescription=request.POST['prescription'],
            allergies=request.POST.get('allergies'),
            treatment_history=request.POST.get('treatment_history')
        )

        appointment.status = 'COMPLETED'
        appointment.save()

        return redirect(
            'doctor_appointment_detail',
            appointment_id=appointment.id
        )

    return render(
        request,
        'doctor/add_medical_record.html',
        {'appointment': appointment}
    )
