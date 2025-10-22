from django.urls import path
from .views import LoginView, UserProfileView, StudentRegisterView, SuperAdminUserView, VerifyStudentAccountView
from .views import PasswordResetRequestView, PasswordResetConfirmView
from .views import StudentListView, StudentDetailView
from .views import AdminListView, AdminDetailView



urlpatterns = [
    path('register/', StudentRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('users/', SuperAdminUserView.as_view(), name='superadmin-users'),
    path('verify/<uuid:token>/', VerifyStudentAccountView.as_view(), name='verify-student'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
    path('students/', StudentListView.as_view(), name='student-list'),
    path('students/<int:pk>/', StudentDetailView.as_view(), name='student-detail'),
    path('admins/', AdminListView.as_view(), name='admin-list'),
    path('admins/<int:pk>/', AdminDetailView.as_view(), name='admin-detail'),
]
