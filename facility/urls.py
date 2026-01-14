from django.urls import path


from adminapp.views import add_department, add_location, delete_location, edit_location, delete_department, \
    edit_department
from facility import views

urlpatterns = [

    path('facility-resource/', views.facility_dashboard, name='facility_dashboard'),

    path('departments/add/', add_department, name='add_department'),
    path('department/edit/<int:id>/', edit_department, name='edit_department'),
    path('department/delete/<int:id>/', delete_department, name='delete_department'),

    path('location/edit/<int:id>/', edit_location, name='edit_location'),
    path('location/add/', add_location, name='add_location'),
    path('location/delete/<int:id>/', delete_location, name='delete_location'),

    path('add-resource/', views.add_health_resource, name='add_health_resource'),
    path('resource/edit/<int:id>/', views.edit_resource, name='edit_resource'),
    path('resource/delete/<int:id>/', views.delete_resource, name='delete_resource'),


    path('resources/add/', views.resource_add, name='resource_add'),
    path('resources/<int:pk>/edit/', views.resource_edit, name='resource_edit'),
    path('resources/<int:pk>/delete/', views.resource_delete, name='resource_delete'),

]