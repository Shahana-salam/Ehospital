import stripe
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from accounts.models import User
from doctorapp.models import Doctor
from facility.models import  Resource
from patientapp.models import Patient, Appointment, MedicalRecord, Billing, HealthResource, Payment


# Create your views here.


def get_or_create_patient(user):
    return Patient.objects.get_or_create(
        user=user,
        defaults={'full_name': user.username}
    )[0]



def register_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('register')

        user = User.objects.create_user(
            username=username,
            password=password,
            role='PATIENT'
        )

        # ✅ create patient only if not exists
        Patient.objects.get_or_create(
            user=user,
            defaults={
                'full_name': request.POST['full_name'],
                'phone': request.POST['phone'],
                'age': request.POST['age'],
                'address': request.POST['address'],
                'gender': request.POST['gender']
            }
        )

        return redirect('login')

    return render(request, 'accounts/register.html')




@login_required
def patient_dashboard(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient = get_or_create_patient(request.user)

    appointments = Appointment.objects.filter(patient=patient)
    medical_records = MedicalRecord.objects.filter(patient=patient)
    bills = Billing.objects.filter(patient=patient)

    context = {
        'patient': patient,
        'appointments': appointments.order_by('-date')[:5],
        'medical_records': medical_records.order_by('-created_at')[:5],
        'total_appointments': appointments.count(),
        'unpaid_bills_count': bills.filter(status='Unpaid').count(),
        'paid_bills_count': bills.filter(status='Paid').count(),
    }

    return render(request, 'patient/dashboard.html', context)



@login_required
def patient_profile(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient = Patient.objects.get(user=request.user)

    return render(request, 'patient/profile.html', {
        'patient': patient
    })


@login_required
def appointmentbook(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient, created = Patient.objects.get_or_create(user=request.user)

    # Fetch all doctors with related department & location
    doctors = Doctor.objects.select_related('specialization', 'location', 'user').all()

    if request.method == "POST":
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time = request.POST.get('time')

        if not doctor_id or not date or not time:
            messages.error(request, "All fields are required!")
        else:
            doctor = get_object_or_404(Doctor, id=doctor_id)

            # Create Appointment
            Appointment.objects.create(
                patient=patient,
                doctor=doctor,
                department=doctor.specialization,
                location=doctor.location,  # store location
                date=date,
                time=time
            )
            messages.success(request, "Appointment booked successfully!")
            return redirect('patient_dashboard')

    return render(request, 'patient/appointmentbook.html', {
        'doctors': doctors
    })



@login_required
def manage_appointments(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient = get_or_create_patient(request.user)
    appointments = Appointment.objects.filter(patient=patient).order_by('-date')

    if request.method == 'POST':
        appointment = Appointment.objects.get(
            id=request.POST.get('appointment_id'),
            patient=patient
        )

        if request.POST.get('action') == 'cancel':
            appointment.status = 'Cancelled'
        else:
            appointment.date = request.POST.get('date')
            appointment.time = request.POST.get('time')
            appointment.status = 'Pending'

        appointment.save()
        return redirect('patient_appointments')

    return render(request, 'patient/appointments.html', {'appointments': appointments})



@login_required
def medical_history(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient = get_or_create_patient(request.user)
    records = MedicalRecord.objects.filter(patient=patient).order_by('-created_at')

    return render(request, 'patient/medical_history.html', {'records': records})






def patient_medical_records(request):
    if request.user.role != 'PATIENT':
        return redirect('login')

    patient = get_or_create_patient(request.user)

    medical_records = MedicalRecord.objects.filter(
        patient=patient
    ).order_by('-created_at')

    return render(request, 'patient/medical_records.html', {
        'medical_records': medical_records
    })





@login_required
def patient_health_resources(request):
    """
    View to show all health resources to patients
    """
    resources = HealthResource.objects.all().order_by('-created_at')  # newest first
    return render(request, 'patient/health_resources.html', {'resources': resources})




def create_checkout_session(request, bill_id):
    bill = get_object_or_404(
        Billing,
        id=bill_id,
        patient__user=request.user,
        status='Unpaid'
    )

    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{
            'price_data': {
                'currency': 'INR',
                'unit_amount': int(bill.amount * 100),
                'product_data': {
                    'name': bill.description,
                },
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('payment_success', args=[bill.id])
        ),
        cancel_url=request.build_absolute_uri(
            reverse('patient_billing')
        ),
    )

    bill.stripe_payment_intent_id = checkout_session.payment_intent
    bill.save()

    return redirect(checkout_session.url)


# Payment Success
def payment_success(request, bill_id):
    bill = get_object_or_404(Billing, id=bill_id, patient__user=request.user)

    bill.status = 'Paid'
    bill.save()

    Payment.objects.create(
        billing=bill,
        amount_paid=bill.amount,
        status='Paid'
    )

    return render(request, 'patient/payment_success.html', {'bill': bill})



def patient_billing(request):
    bills = Billing.objects.filter(patient__user=request.user)
    return render(request, 'patient/patient_billing.html', {'bills': bills})


def about_us(request):
    return render(request, 'patient/about.html')

def fecility(request):
    return render(request, 'patient/facility_resources.html')


def patient_facility_view(request):
    # We fetch all resources and group them by department
    resources = Resource.objects.all().select_related('department')
    return render(request, 'patient/resource_view.html', {'resources': resources})