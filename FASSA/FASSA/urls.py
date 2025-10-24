from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/admin_panel/', include('admin_panel.urls')),
    path('api/students/', include('students.urls')),

]
