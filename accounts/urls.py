from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import login_view, home
from .views import admin_dashboard
from . import views


urlpatterns = [

    path('', home, name='home'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('admin-panel/dashboard/', admin_dashboard, name='admin_dashboard'),

]
