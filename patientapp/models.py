
from django.db import models

from accounts.models import User



# models.py
class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)

    def __str__(self):
        return self.full_name or self.user.username



class Appointment(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
        ('Completed', 'Completed'),
    )
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctorapp.Doctor', on_delete=models.CASCADE,null=True)
    department = models.ForeignKey('facility.Department', on_delete=models.CASCADE)
    location = models.ForeignKey('facility.Location', on_delete=models.CASCADE,null=True)  # NEW FIELD
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True,null=True)


    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.user.username} on {self.date}"





class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey('doctorapp.Doctor', on_delete=models.SET_NULL,
        null=True,
        blank=True)
    diagnosis = models.TextField()
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE, null=True, blank=True)  # NEW
    prescription = models.TextField()
    allergies = models.TextField(blank=True, null=True)
    treatment_history = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Billing(models.Model):
    STATUS_CHOICES = [
        ('Unpaid', 'Unpaid'),
        ('Paid', 'Paid'),
    ]

    patient = models.ForeignKey('Patient', on_delete=models.CASCADE)
    appointment = models.ForeignKey('Appointment', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)   # consultation, lab test, surgery etc
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unpaid')
    stripe_payment_intent_id = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - {self.amount} - {self.status}"


class Payment(models.Model):
    billing = models.ForeignKey(Billing, on_delete=models.CASCADE)
    payment_date = models.DateTimeField(auto_now_add=True)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('Pending','Pending'), ('Paid','Paid')])

    def __str__(self):
        return f"{self.billing} - {self.status}"



class HealthResource(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
