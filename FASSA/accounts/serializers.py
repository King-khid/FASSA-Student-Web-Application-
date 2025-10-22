from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from .utils import generate_temporary_password, send_account_email
from .utils import send_student_verification_email
from .models import PasswordReset



User = get_user_model()


class StudentRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['full_name', 'email', 'password', 'confirm_password']

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        if not attrs['email'].endswith('@ttu.edu.gh'):
            raise serializers.ValidationError({"email": "Students must register with a valid TTU email."})
        return attrs

    def create(self, validated_data):
        validated_data.pop('confirm_password')

        # Create user as inactive until verification
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            role='STUDENT',
            password=validated_data['password'],
            is_active=False
        )

        # Send verification email
        send_student_verification_email(
            user_email=user.email,
            full_name=user.full_name,
            verification_token=str(user.verification_token)
        )

        return user


class SuperAdminUserSerializer(serializers.ModelSerializer):
    role = serializers.ChoiceField(choices=[('STUDENT', 'Student'), ('ADMIN', 'Admin')])

    class Meta:
        model = User
        fields = ['full_name', 'email', 'role']

    def create(self, validated_data):
        role = validated_data.pop('role')
        temp_password = generate_temporary_password()
        user = User.objects.create_user(
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            role=role,
            password=temp_password
        )
        send_account_email(user.email, user.full_name, user.role, temp_password)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'full_name', 'email', 'role', 'is_active']


class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordResetConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(write_only=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Passwords do not match."})
        return attrs