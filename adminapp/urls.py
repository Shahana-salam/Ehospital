
from django.urls import path

from . import views


urlpatterns = [


    path('doctors/', views.manage_doctors, name='manage_doctors'),
    path('doctors/add/', views.add_doctor, name='add_doctor'),
    path('doctors/edit/<int:pk>/', views.edit_doctor, name='edit_doctor'),
    path('doctors/delete/<int:pk>/', views.delete_doctor, name='delete_doctor'),

    path('patients/', views.patients_list, name='patients_list'),
    path('patients/toggle/<int:patient_id>/', views.toggle_patient_status, name='toggle_patient_status'),

    path('admin/appointments/', views.admin_appointments, name='admin_appointments'),
path('admin/add-billing/', views.add_billing, name='add_billing'),
path(
    'admin/billing/',
    views.admin_billing_list,
    name='admin_billing_list'
),




]