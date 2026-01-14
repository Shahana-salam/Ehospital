from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import patient_dashboard, manage_appointments, medical_history, register_view, \
    patient_billing

urlpatterns = [

    path('register/', register_view, name='register'),
    path('profile/', views.patient_profile, name='patient_profile'),

    path('appointments/', views.manage_appointments, name='patient_appointments'),
    path('bookappointment/', views.appointmentbook, name='bookappointment'),

    path('medical-records/', views.patient_medical_records, name='patient_medical_records'),

    path('dashboard/', patient_dashboard, name='patient_dashboard'),
    path('appointments/', manage_appointments, name='patient_appointments'),
    path('medical-history/', medical_history, name='medical_history'),
    path('billing/', patient_billing, name='patient_billing'),

    path('health-resources/', views.patient_health_resources, name='patient_health_resources'),

    path('billing/', views.patient_billing, name='patient_billing'),
    path('billing/pay/<int:bill_id>/', views.create_checkout_session, name='create_checkout_session'),
    path('billing/success/<int:bill_id>/', views.payment_success, name='payment_success'),

    path('about/', views.about_us, name='about_us'),
    path('facility/', views.fecility, name='facility_resources'),
    path('resource/', views.patient_facility_view, name='resource_view'),




]