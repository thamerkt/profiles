from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from .models import Profil, ProfilMoral, PhysicalProfil
from .serializers import ProfileSerializer, ProfilMoralSerializer, PhysicalProfilSerializer

# Profil ViewSet for regular profiles
class ProfilViewSet(viewsets.ModelViewSet):
    queryset = Profil.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_param = self.request.query_params.get('user', None)
        if user_param:
            return self.queryset.filter(user_id=user_param)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ProfilMoral ViewSet for moral profiles
class ProfilMoralViewSet(viewsets.ModelViewSet):
    queryset = ProfilMoral.objects.all()
    serializer_class = ProfilMoralSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        user_param = self.request.query_params.get('profil', None)
        if user_param:
            return self.queryset.filter(profil=user_param)
        return self.queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# ProfilPhysique ViewSet for physical profiles (with file upload handling)
class ProfilPhysiqueViewSet(viewsets.ModelViewSet):
    queryset = PhysicalProfil.objects.all()
    serializer_class = PhysicalProfilSerializer
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # Handles file uploads (multipart/form-data)

    def get_queryset(self):
        user_param = self.request.query_params.get('profil', None)
        if user_param:
            return self.queryset.filter(profil=user_param)
        return self.queryset

    def create(self, request, *args, **kwargs):
        print("Received data:", request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save()
            return Response(self.get_serializer(instance).data, status=status.HTTP_201_CREATED)
        else:
            print("Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
