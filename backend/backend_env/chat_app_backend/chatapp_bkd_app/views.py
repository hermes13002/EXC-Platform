from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import generics  # Importing generics for generic views
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken  # Importing RefreshToken for token generation
from rest_framework.response import Response  # Importing Response for sending API responses
from rest_framework import status  # Importing status for HTTP status codes
from rest_framework.permissions import IsAuthenticated  # Importing permissions
from .models import UserModel  # Importing the User model
from django.db.models import Q  # Importing Q for complex queries
from rest_framework.exceptions import NotFound
from rest_framework import viewsets

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data = request.data)

        # check if data is valid
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            return Response(
                {
                    "message": "User Registration Successful",
                    "username": serializer.data['username'],
                    "first_name": serializer.data['first_name'],
                    "last_name": serializer.data['last_name'],
                    "email": serializer.data['email'],
                    "phone_number": serializer.data['phone_number'],
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    }
                },
                status = status.HTTP_201_CREATED
            )
        # Return error response if data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class LoginView(APIView):
    def post(self, request):
        # deserialize request data
        serializer = LoginSerializer(data = request.data)

        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh = RefreshToken.for_user(user)
            
            return Response(
                {
                    "message": "User Logged In Successfully",
                    "user": UserSerializer(user).data,
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    } 
                },
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return error response if data is invalid
    

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get(self, request): 
        user = request.user  # Get the authenticated user
        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "message": "User Profile retrieved successfully",
                "user": UserSerializer(user).data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                } 
            },
            status=status.HTTP_200_OK
        )

   
class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        query = self.request.query_params.get("q", "").strip()
        if not query:
            return UserModel.objects.none()  # Return an empty queryset if query is empty
        return UserModel.objects.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query) | Q(email__icontains=query)  # Search by username, first name, or email
        )


# Update User Profile API
class UpdateUserView(viewsets.ModelViewSet):
    queryset = UserModel.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return UserModel.objects.filter(id=self.request.user.id)

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)  # Return the updated user data
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)  # Return validation errors
