from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from .models import LabResult
from .serializers import LabResultSerializer
from .validators import validate_lab_result
from .permissions import IsViewerReadOnlyElseDataEntryOrAdmin

# Manual lab result entry (protected)
class ManualLabResultView(generics.ListCreateAPIView):
    queryset = LabResult.objects.all()
    serializer_class = LabResultSerializer
    permission_classes = [IsViewerReadOnlyElseDataEntryOrAdmin]

    def get_queryset(self):
        queryset = super().get_queryset()
        sex = self.request.query_params.get('sex')
        if sex:
            queryset = queryset.filter(sex=sex)
        return queryset

    def perform_create(self, serializer):
        validate_lab_result(self.request.data)
        serializer.save()

# Token login
class CustomAuthToken(ObtainAuthToken):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username}, status=status.HTTP_200_OK)

# Options endpoint
class OptionsList(APIView):
    permission_classes = []

    def get(self, request):
        data = {
            "hosts": ["HUMAN", "ANIMAL", "ENVIRONMENT"],
            "environment_types": ["Blood", "Urine", "Sputum"],
            "animal_species": ["Cattle", "Goat", "Sheep"]
        }
        return Response(data)

# Lab results endpoint
class LabResultList(APIView):
    permission_classes = []

    def get(self, request):
        results = LabResult.objects.all().order_by('-test_date')
        serializer = LabResultSerializer(results, many=True)
        return Response(serializer.data)
