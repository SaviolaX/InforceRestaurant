from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status

from .serializers import AuthUserSerializer
from .models import User
            


class RegisterUserView(CreateAPIView):
    """Registrate a new user"""
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = (AllowAny, )
    

class LogoutView(APIView):
    """Logout user"""
    def post(self, request):
        try:
            refresh_token = request.data
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    
