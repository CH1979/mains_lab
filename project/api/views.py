from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Bill, BillsFile, Client, ClientOrgsFile
from .serializers import (
    BillSerializer,
    BillsFileSerializer,
    ClientSerializer,
    ClientOrgsFileSerializer
)


class ClientOrgsFileUploadAPIView(CreateAPIView):
    queryset = ClientOrgsFile.objects.all()
    serializer_class = ClientOrgsFileSerializer


class BillsFileUploadAPIView(CreateAPIView):
    queryset = BillsFile.objects.all()
    serializer_class = BillsFileSerializer


class ClientListAPIView(ListAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class BillListAPIView(ListAPIView):
    queryset = Bill.objects.all()
    serilizer_class = BillSerializer
