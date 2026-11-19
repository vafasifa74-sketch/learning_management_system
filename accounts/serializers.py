from django.db import transaction
from rest_framework import serializers
from accounts.models import User, TrainerProfile, StudentProfile


class TrainerProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = TrainerProfile
        fields = "__all__"
        read_only_fields = ["user"]


class StudentProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)
    phone = serializers.CharField(source="user.phone", read_only=True)

    class Meta:
        model = StudentProfile
        fields = "__all__"
        read_only_fields = ["user"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    experience = serializers.IntegerField(write_only=True, required=False, default=0)

    class Meta:
        model = User
        fields = ["username", "email", "password", "phone", "role", "experience"]

    @transaction.atomic
    def create(self, validated_data):
        experience = validated_data.pop("experience", 0)
        user = User.objects.create_user(**validated_data)

        if user.role == "trainer":
            TrainerProfile.objects.create(user=user, experience=experience)
        elif user.role == "student":
            StudentProfile.objects.create(user=user)

        return user


    
