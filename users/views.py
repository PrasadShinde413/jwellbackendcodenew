

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer, UserLoginSerializer
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated,AllowAny

from rest_framework_simplejwt.tokens import RefreshToken
from .models import User

# class RegisterView(APIView):
# 	permission_classes = [permissions.AllowAny]
# 	def post(self, request):
# 		serializer = UserRegisterSerializer(data=request.data)
# 		if serializer.is_valid():
# 			user = serializer.save()
# 			return Response({'message': 'User registered successfully'}, status=status.HTTP_201_CREATED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# from rest_framework import status, permissions
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from .serializers import UserRegisterSerializer
# from .models import User


# class RegisterView(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request):
#         serializer = UserRegisterSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(
#                 {'message': 'User registered successfully'},
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .serializers import UserRegisterSerializer
from master.models import Notification

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create a notification for this user
            Notification.objects.create(
                user=user,
                title="Welcome!",
                message="Thank you for registering. Your account has been created successfully.",
                type="SUCCESS"
            )

            return Response(
                {'message': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LoginView(APIView):
# 	permission_classes = [permissions.AllowAny]
# 	def post(self, request):
# 		serializer = UserLoginSerializer(data=request.data)
# 		if serializer.is_valid():
# 			username = serializer.validated_data['username']
# 			password = serializer.validated_data['password']
# 			user = authenticate(request, username=username, password=password)
# 			if user:
# 				refresh = RefreshToken.for_user(user)
# 				return Response({
# 					'access': str(refresh.access_token),
# 					'refresh': str(refresh),
# 					'role': user.role,
# 				}, status=status.HTTP_200_OK)
# 			return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
# 		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import authenticate
from .serializers import UserLoginSerializer
from .tokens import get_tokens_for_user

# users/views.py

from .tokens import get_tokens_for_user

class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(request, username=username, password=password)

            if user:
                tokens = get_tokens_for_user(user)

                return Response({
                    'access': tokens['access'],
                    'refresh': tokens['refresh'],
                    'username': user.username,
                    'role': user.role,
                    'user_id': user.id,
                    'email': user.email,
                }, status=status.HTTP_200_OK)

            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404

from .models import User
from .serializers import UserRegisterSerializer

class UserListView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserRegisterSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserDetailView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, username):
        """Retrieves a single user by Username."""
        # Lookup by username instead of id
        user = get_object_or_404(User, username=username)
        
        serializer = UserRegisterSerializer(user)
        
        response_data = [serializer.data] 
        
        return Response(response_data, status=status.HTTP_200_OK)


class UserUpdateView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        serializer = UserRegisterSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "User updated successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDeleteView(APIView):
    permission_classes = [permissions.AllowAny]

    def delete(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_200_OK)


from .models import StockOpening
from .serializers import StockOpeningSerializer
# StockOpening CRUD APIs
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from django.db.models import Sum

class StockOpeningTotalWeightView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        total = StockOpening.objects.aggregate(
            total_weight=Sum('final_weight')
        )

        return Response(
            {
                "total_weight": total["total_weight"] or 0
            },
            status=status.HTTP_200_OK
        )

class StockOpeningCreateView(APIView):
	permission_classes = [AllowAny]
	def post(self, request):
		serializer = StockOpeningSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StockOpeningListView(APIView):
	permission_classes = [AllowAny]
	def get(self, request):
		stocks = StockOpening.objects.all().order_by('-created_at')
		serializer = StockOpeningSerializer(stocks, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

class StockOpeningDetailView(APIView):
	permission_classes = [AllowAny]
	def get(self, request, pk):
		stock = get_object_or_404(StockOpening, pk=pk)
		serializer = StockOpeningSerializer(stock)
		return Response(serializer.data, status=status.HTTP_200_OK)
	def put(self, request, pk):
		stock = get_object_or_404(StockOpening, pk=pk)
		serializer = StockOpeningSerializer(stock, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
	def delete(self, request, pk):
		stock = get_object_or_404(StockOpening, pk=pk)
		stock.delete()
		return Response({'message': 'Stock deleted successfully'}, status=status.HTTP_200_OK)



# views.py
from django.db import connection
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

class CustomerSaleItemsAPIView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, customer_id):
        try:
            with connection.cursor() as cursor:
                cursor.execute("""
                    SELECT 
                        id,
                        item_name,
                        DATE(created_at) AS date,
                        total_amount
                    FROM jms.master_saleitem
                    WHERE customer_id = %s
                    ORDER BY created_at DESC
                """, [customer_id])

                columns = [col[0] for col in cursor.description]
                data = [dict(zip(columns, row)) for row in cursor.fetchall()]

            if not data:
                return Response({"message": "No sale items found for this customer."}, status=status.HTTP_404_NOT_FOUND)

            return Response(data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from .models import User, UserDocuments
from .serializers import ProfilePictureUploadSerializer, UserDocumentSerializer


# ✅ API 1: Upload Profile Picture
class UploadProfilePictureView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        serializer = ProfilePictureUploadSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Profile picture uploaded successfully for user {user.username}',
                'profile_pic': serializer.data['profile_pic']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

###################################################################################################################

class UpdateProfilePictureView(APIView):
    permission_classes = [permissions.AllowAny]

    def put(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {"message": "user_id is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = get_object_or_404(User, id=user_id)

        serializer = ProfilePictureUploadSerializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': f'Profile picture updated successfully for user {user.username}',
                'profile_pic': serializer.data.get('profile_pic')
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



####################################################################################################################

# ✅ API 2: Upload Multiple Documents
class UploadDocumentsView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get('user_id')
        if user_id:
            user = get_object_or_404(User, id=user_id)
        else:
            user = request.user

        files = request.FILES.getlist('documents')
        document_names = request.data.getlist('document_name', [])

        if not files:
            return Response({'error': 'No documents provided'}, status=status.HTTP_400_BAD_REQUEST)

        uploaded_docs = []
        for idx, file in enumerate(files):
            name = document_names[idx] if idx < len(document_names) else file.name
            document = UserDocuments.objects.create(user=user, document_name=name, document_file=file)
            uploaded_docs.append(UserDocumentSerializer(document).data)

        return Response({
            'message': f'Documents uploaded successfully for user {user.username}',
            'documents': uploaded_docs
        }, status=status.HTTP_201_CREATED)

    def get(self, request):
        """Admins can see all, others see their own"""
        if request.user.role == "Admin":
            documents = UserDocuments.objects.select_related('user').all()
        else:
            documents = UserDocuments.objects.filter(user=request.user)

        serializer = UserDocumentSerializer(documents, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model

User = get_user_model()


class ResetPasswordAPIView(APIView):
    """
    POST API - Reset Password
    Payload Example:
    {
        "user_id": 3,
        "old_password": "oldpass123",   # Optional if user is Admin
        "new_password": "newpass123",
        "confirm_password": "newpass123"
    }
    """
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        user_id = request.data.get("user_id")
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        if not user_id or not new_password or not confirm_password:
            return Response({"error": "user_id, new_password, and confirm_password are required."},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        # Check if both passwords match
        if new_password != confirm_password:
            return Response({"error": "New password and confirm password do not match."},
                            status=status.HTTP_400_BAD_REQUEST)

        # If the user is an admin, skip old password validation
        if user.role == "Admin":
            user.set_password(new_password)
            user.save()
            return Response({"message": "Password reset successfully by Admin."}, status=status.HTTP_200_OK)

        # For normal users — old password must match
        if not old_password:
            return Response({"error": "Old password is required for non-admin users."},
                            status=status.HTTP_400_BAD_REQUEST)

        if not user.check_password(old_password):
            return Response({"error": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)



# todoapp/views.py

from rest_framework import generics
from .models import TodoTask
from .serializers import TodoTaskSerializer

class TodoTaskListCreate(generics.ListCreateAPIView):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer

class TodoTaskRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = TodoTask.objects.all()
    serializer_class = TodoTaskSerializer
