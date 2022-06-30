from django.urls import path

from .views import (
    ClientOrgsFileUploadAPIView,
    BillsFileUploadAPIView,
    ClientListAPIView,
    BillListAPIView
)

urlpatterns = [
    path(
        'clients/',
        ClientListAPIView.as_view(),
        name='clients',
    ),
    path(
        'clients/upload/',
        ClientOrgsFileUploadAPIView.as_view(),
        name='clients-upload',
    ),
    path(
        'bills/',
        BillListAPIView.as_view(),
        name='bills',
    ),
    path(
        'bills/upload/',
        BillsFileUploadAPIView.as_view(),
        name='bills-upload',
    )
]
