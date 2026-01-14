from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404

from facility.forms import HealthResourceForm, ResourceForm
from facility.models import Location, Department, Resource
from patientapp.models import HealthResource


# Create your views here.
def is_admin(user):
    return user.is_authenticated and getattr(user, 'role', None) == 'ADMIN'


def facility_dashboard(request):
    locations = Location.objects.all()
    departments = Department.objects.all()
    resources = HealthResource.objects.all()
    facility_resources = Resource.objects.all()
    return render(request, 'admin/facility_dashboard.html', {
        'locations': locations,
        'departments': departments,
        'resources': resources,
        'facility_resources': facility_resources,
    })




@login_required
@user_passes_test(is_admin)
def add_health_resource(request):
    if request.method == 'POST':
        form = HealthResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_dashboard')
    else:
        form = HealthResourceForm()
    return render(request, 'admin/add_health_resource.html', {'form': form})



def edit_resource(request, id):
    resource = get_object_or_404(HealthResource, id=id)
    form = HealthResourceForm(request.POST or None, instance=resource)
    if form.is_valid():
        form.save()
        return redirect('facility_dashboard')
    return render(request, 'admin/health_resource_edit.html', {'form': form, 'title': 'Edit Health Resource'})



def delete_resource(request, id):
    resource = get_object_or_404(HealthResource, id=id)
    resource.delete()
    return redirect('facility_dashboard')





# Add new resource
def resource_add(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('facility_dashboard')
    else:
        form = ResourceForm()
    return render(request, 'admin/resource_form.html', {'form': form})





# Edit resource
def resource_edit(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        form = ResourceForm(request.POST, instance=resource)
        if form.is_valid():
            form.save()
            return redirect('facility_dashboard')
    else:
        form = ResourceForm(instance=resource)
    return render(request, 'admin/resource_form.html', {'form': form})




# Delete resource
def resource_delete(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    if request.method == 'POST':
        resource.delete()
        return redirect('facility_dashboard')
    return render(request, 'admin/resource_confirm_delete.html', {'resource': resource})