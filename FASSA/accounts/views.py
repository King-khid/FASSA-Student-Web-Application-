from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from .models import PasswordReset
from .serializers import PasswordResetRequestSerializer, PasswordResetConfirmSerializer


from .serializers import (
    StudentRegistrationSerializer,
    SuperAdminUserSerializer,
    LoginSerializer,
    UserProfileSerializer,
)
from .permissions import IsSuperAdmin
from .utils import send_password_reset_email

User = get_user_model()


class StudentRegisterView(generics.CreateAPIView):
    serializer_class = StudentRegistrationSerializer
    permission_classes = [AllowAny]


class VerifyStudentAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, token):
        user = get_object_or_404(User, verification_token=token)
        if user.is_verified:
            return Response({"message": "Account already verified."}, status=status.HTTP_200_OK)

        user.is_verified = True
        user.is_active = True
        user.save()
        return Response({"message": "Account verified successfully. You can now log in."}, status=status.HTTP_200_OK)


class SuperAdminUserView(generics.ListCreateAPIView):
    serializer_class = SuperAdminUserSerializer
    permission_classes = [IsAuthenticated, IsSuperAdmin]
    queryset = User.objects.all()


class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = authenticate(request, email=email, password=password)
        if not user:
            return Response({"error": "Invalid email or password."}, status=status.HTTP_400_BAD_REQUEST)

        refresh = RefreshToken.for_user(user)
        return Response({
            "message": "Login successful.",
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_200_OK)


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class PasswordResetRequestView(generics.GenericAPIView):
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"detail": "If this email exists, a reset link will be sent."}, status=status.HTTP_200_OK)

        # create token
        reset_obj = PasswordReset.objects.create(user=user)
        send_password_reset_email(user.email, reset_obj.token)

        return Response({"detail": "If this email exists, a reset link will be sent."}, status=status.HTTP_200_OK)


class PasswordResetConfirmView(generics.GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']

        reset_obj = get_object_or_404(PasswordReset, token=token)
        if reset_obj.is_expired():
            return Response({"detail": "Token expired."}, status=status.HTTP_400_BAD_REQUEST)

        user = reset_obj.user
        user.set_password(new_password)
        user.save()
        reset_obj.delete()

        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
