from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Bill, BillsFile, Client, ClientOrgsFile
from .serializers import (
    BillSerializer,
    BillsFileSerializer,
    ClientSerializer,
    ClientOrgsFileSerializer
)


class ClientOrgsFileUploadAPIView(CreateAPIView):
    pass


class BillsFileUploadAPIView(CreateAPIView):
    pass


class ClientListAPIView(ListAPIView):
    pass


class BillListAPIView(ListAPIView):
    pass
