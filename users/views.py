from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserProfileSerializer
from rest_framework.views import APIView
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string

User = get_user_model()

# Registration View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        # Generate simple verification token (for demonstration)
        token = get_random_string(32)
        user.verification_token = token
        user.save()
        # Send verification email (placeholder logic)
        send_mail(
            'Verify your Moddie account',
            f'Your verification token: {token}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=True,
        )

# Email Verification View (token-based, simple)
class VerifyEmailView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        email = request.data.get('email')
        token = request.data.get('token')
        try:
            user = User.objects.get(email=email)
            if getattr(user, 'verification_token', None) == token:
                user.is_active = True
                user.email_verified = True
                user.verification_token = ''
                user.save()
                return Response({'detail': 'Email verified.'}, status=status.HTTP_200_OK)
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

# User Profile View
class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
