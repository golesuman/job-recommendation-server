from django.contrib.auth import authenticate, login
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import (
    InteractionSerializer,
    UserProfileSerializer,
    UserSignUpSerializer,
)
from .services.user_profile_service import (
    get_latest_user_interactions,
    get_user_profile,
)

# Create your views here.
from rest_framework.views import APIView


class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        auth = request.headers.get("Authorization")
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {"token": token.key, "user_id": user.id}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
            )


class UserLogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.auth.delete()
        return Response(
            {"message": "Successfully logged out"}, status=status.HTTP_200_OK
        )


class UserProfileAPI(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.user.id
        if user_id is not None:
            user_profile = get_user_profile(user_id)
            interactions = get_latest_user_interactions(user_id)
            user_profile_serializer = UserProfileSerializer(user_profile)
            interactions_serializer = InteractionSerializer(interactions, many=True)
            response = {
                "profile": user_profile_serializer.data,
                "interactions": interactions_serializer.data,
            }
            return Response(response, status=status.HTTP_200_OK)

        # pass


class UserSignUpAPI(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSignUpSerializer(data=request.data)
        if serializer.is_valid():
            try:
                serializer.save()
                return Response(
                    {"data": "User Created Successfully"},
                    status=status.HTTP_201_CREATED,
                )
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
