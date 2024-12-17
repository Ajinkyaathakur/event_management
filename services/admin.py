from django.contrib import admin
from .models import UserProfile  # Import model

# Register UserProfile model to make it editable in admin
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')  # Display 'user' and 'role' in the admin list view
    search_fields = ('user__username', 'role')  # Enable searching by 'username' or 'role'

admin.site.register(UserProfile, UserProfileAdmin)  # Register the UserProfile model in the admin interface
