
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),   # First, let Django handle /admin/
    path('', include('main.urls')),    # Then your app handles everything else
]

