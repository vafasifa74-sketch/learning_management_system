from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.models import User, TrainerProfile, StudentProfile
from accounts.serializers import (
    UserSerializer,
    TrainerProfileSerializer,
    StudentProfileSerializer,
)


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "message": "User and profile created successfully.",
                    "token": token.key,
                    "username": user.username,
                    "role": user.role,
                },
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Accepts username, email, or phone because of EmailBackend & PhoneBackend
        identifier = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=identifier, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                {
                    "token": token.key,
                    "user_id": user.id,
                    "username": user.username,
                    "role": user.role,
                },
                status=status.HTTP_200_OK,
            )
        return Response(
            {"error": "Invalid credentials."},
            status=status.HTTP_401_UNAUTHORIZED,
        )


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    def get_profile_and_serializer(self, user, data=None, partial=False):
        if user.role == "trainer":
            profile, _ = TrainerProfile.objects.get_or_create(user=user)
            if data is not None:
                return TrainerProfileSerializer(profile, data=data, partial=partial)
            return TrainerProfileSerializer(profile)
        elif user.role == "student":
            profile, _ = StudentProfile.objects.get_or_create(user=user)
            if data is not None:
                return StudentProfileSerializer(profile, data=data, partial=partial)
            return StudentProfileSerializer(profile)
        return None

    def get(self, request):
        serializer = self.get_profile_and_serializer(request.user)
        if not serializer:
            return Response(
                {"detail": "Admin users do not have a role profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(serializer.data)

    def put(self, request):
        serializer = self.get_profile_and_serializer(request.user, data=request.data)
        if not serializer:
            return Response(
                {"detail": "Admin users do not have a role profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        serializer = self.get_profile_and_serializer(
            request.user, data=request.data, partial=True
        )
        if not serializer:
            return Response(
                {"detail": "Admin users do not have a role profile."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
