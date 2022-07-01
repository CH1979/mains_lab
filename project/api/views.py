from django.db.models import Count, Sum
from rest_framework.generics import CreateAPIView, ListAPIView

from .models import Bill, BillsFile, Client, ClientOrgsFile
from .serializers import (
    BillSerializer,
    BillsFileSerializer,
    ClientSerializer,
    ClientOrgsFileSerializer
)


class ClientOrgsFileUploadAPIView(CreateAPIView):
    """APIView for upload ClientOrg xlsx file"""
    queryset = ClientOrgsFile.objects.all()
    serializer_class = ClientOrgsFileSerializer


class BillsFileUploadAPIView(CreateAPIView):
    """APIView for upload Bills xlsx file"""
    queryset = BillsFile.objects.all()
    serializer_class = BillsFileSerializer


class ClientListAPIView(ListAPIView):
    """ListAPIView for Clients"""
    serializer_class = ClientSerializer

    def get_queryset(self):
        queryset = Client.objects \
            .annotate(orgs_count=Count('organization', distinct=True)) \
            .annotate(income=Sum('organization__bill__bill_sum'))

        return queryset.values('name', 'orgs_count', 'income')


class BillListAPIView(ListAPIView):
    """ListAPIView for Bills"""
    serializer_class = BillSerializer

    def get_queryset(self):
        queryset = Bill.objects.all()

        client_id = self.request.query_params.get('client_id')
        if client_id is not None:
            queryset = queryset.filter(client=client_id)

        organization_id = self.request.query_params.get('organization_id')
        if organization_id is not None:
            queryset = queryset.filter(organization_id=organization_id)

        return queryset
