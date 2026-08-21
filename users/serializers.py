
from rest_framework import serializers
from .models import User

# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True)
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'employee_id', 'date_of_joining', 'username', 'password', 'address', 'phone_number', 'role']

#     def create(self, validated_data):
#         password = validated_data.pop('password')
#         user = User(**validated_data)
#         user.set_password(password)
#         user.save()
#         return user

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


# class UserRegisterSerializer(serializers.ModelSerializer):
#     password = serializers.CharField(write_only=True, required=False)

#     class Meta:
#         model = User
#         fields = [
#             'id', 'name', 'employee_id', 'date_of_joining',
#             'username', 'password', 'address', 'phone_number', 'role'
#         ]

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         user = User(**validated_data)
#         if password:
#             user.set_password(password)
#         user.save()
#         return user

#     def update(self, instance, validated_data):
#         password = validated_data.pop('password', None)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)
#         if password:
#             instance.set_password(password)
#         instance.save()
#         return instance


from rest_framework import serializers
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = [
            'id', 'first_name', 'middle_name', 'last_name', 'employee_id', 'date_of_joining','email',
            'username', 'password', 'address', 'phone_number', 'role', 'gender',
            'state', 'city', 'zip_code', 'profile_pic'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance

from .models import StockOpening

# Serializer for StockOpening
class StockOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockOpening
        fields = ['id', 'medal', 'item', 'final_weight', 'amount', 'created_at']


from rest_framework import serializers
from .models import User, UserDocuments


class ProfilePictureUploadSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ['user_id', 'profile_pic']

    def update(self, instance, validated_data):
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.save()
        return instance


class UserDocumentSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = UserDocuments
        fields = ['id', 'user_id', 'user', 'document_name', 'document_file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']



# todoapp/serializers.py

from rest_framework import serializers
from .models import TodoTask

class TodoTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TodoTask
        fields = ['id', 'task', 'created_at'] # 'id' is good to include for referencing
        read_only_fields = ['created_at'] # created_at should be set automatically