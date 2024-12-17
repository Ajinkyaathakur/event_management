from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('home/', views.home, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('create-event/', views.create_event, name='create_event'),  # Only accessible to admins and managers
    path('events/', views.event_list, name='events'),  # Accessible to all users
    path('register-event/<int:event_id>/', views.register_for_event, name='register_for_event'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('assign_manager/<int:user_id>/', views.assign_manager_role, name='assign_manager'),
]
