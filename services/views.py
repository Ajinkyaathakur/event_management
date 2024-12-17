from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from .models import Event, Registration, UserProfile
from django.contrib.auth.models import User
from .forms import SignupForm

# View for listing all events
@login_required
def event_list(request):
    events = Event.objects.all()  # Get all events
    return render(request, 'event_list.html', {'events': events})

# View for registering a user for an event
@login_required
def register_for_event(request, event_id):
    event = Event.objects.get(id=event_id)
    # Assuming you have a `Registration` model for this
    event_reg = Registration.objects.create(user=request.user, event=event)
    event_reg.save()
    return redirect('dashboard')  # Redirect to the user dashboard

# User dashboard to see registered events and personal info
@login_required
def user_dashboard(request):
    user = request.user
    registered_events = Registration.objects.filter(user=user)  # Get events the user has registered for
    return render(request, 'user_dashboard.html', {
        'user': user, 
        'registered_events': registered_events,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'role': user.userprofile.role  # Add role to the context
    })

# Signup view for user registration and automatic login
def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            first_name = form.cleaned_data.get('first_name')  # Optional
            last_name = form.cleaned_data.get('last_name')    # Optional
            email = form.cleaned_data['email']  # Required

            # Check if the email already exists
            if User.objects.filter(email=email).exists():
                messages.error(request, "An account with this email already exists.")
                return redirect('signup')

            # Create the user
            user = User.objects.create_user(
                username=username,
                password=password,
                first_name=first_name,
                last_name=last_name,
                email=email
            )
            user.save()

            # Create the UserProfile and assign the 'user' role
            UserProfile.objects.create(user=user, role='user')

            # Log in the user after successful registration
            auth_login(request, user)
            messages.success(request, "Account created successfully and logged in.")
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

# Login view for user authentication
def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')  # Redirect to home if the user is already logged in.

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            # Log the user in if authentication is successful
            auth_login(request, user)
            messages.success(request, "You have logged in successfully.")
            return redirect('home')  # Redirect to home or dashboard page after successful login
        else:
            messages.error(request, "Invalid username or password.")
            return redirect('login')  # Redirect to the login page if authentication fails

    return render(request, 'login.html')

# Home page view, accessible only to logged-in users
@login_required
def home(request):
    return render(request, 'home.html')

# Logout view to log the user out and redirect to the login page
def logout_view(request):
    logout(request)
    return redirect('login')

# Create event view, accessible only by admin or manager
@login_required
def create_event(request):
    if request.user.userprofile.role not in ['admin', 'manager']:
        raise PermissionDenied  # Only admins and managers can create events
    
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        date = request.POST['date']
        
        # Create event and assign the user as the creator
        Event.objects.create(
            title=title,
            description=description,
            date=date,
            created_by=request.user
        )
        messages.success(request, "Event created successfully.")
        return redirect('event_list')  # Redirect to the event list page

    return render(request, 'create_event.html')

# Assign manager role to a user (only accessible by superuser/admin)
@login_required
def assign_manager_role(request, user_id):
    if not request.user.is_superuser:  # Only superusers can assign roles
        raise PermissionDenied

    try:
        user = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user)
        user_profile.role = 'manager'  # Assign the 'manager' role
        user_profile.save()
        messages.success(request, f"Role for {user.username} updated to Manager.")
    except User.DoesNotExist:
        messages.error(request, "User not found.")
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
    
    return redirect('user_dashboard')  # Redirect back to user dashboard or any other page

    if not request.user.is_superuser:  # Only superusers can assign roles
        raise PermissionDenied

    user = User.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)
    user_profile.role = 'manager'  # Assign the 'manager' role
    user_profile.save()
    messages.success(request, f"Role for {user.username} updated to Manager.")
    return redirect('user_dashboard')  # Redirect back to user dashboard or any other page

