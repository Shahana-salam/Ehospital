from django.urls import path

from doctorapp.views import doctor_dashboard, patient_detail, patient_list, appointment_list, \
    appointment_detail, medical_records_list, add_medical_record_from_appointment

urlpatterns = [
    path('dashboard/', doctor_dashboard, name='doctor_dashboard'),
    path('patients/',patient_list, name='doctor_patients'),
    path('patients/<int:patient_id>/', patient_detail, name='doctor_patient_detail'),

    path('appointments/',appointment_list, name='doctor_appointments'),
   path('appointments/<int:appointment_id>/',appointment_detail, name='doctor_appointment_detail'),

path('medical-records/',medical_records_list, name='doctor_medical_records'),

path(
    'appointments/<int:appointment_id>/add-record/',
    add_medical_record_from_appointment,
    name='add_medical_record_from_appointment'
)



]
