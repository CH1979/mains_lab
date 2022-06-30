from rest_framework import serializers

from .models import Bill, BillsFile, Client, ClientOrgsFile


class BillSerializer(serializers.ModelSerializer):
    model = Bill
    fields = '__all__'


class BillsFileSerializer(serializers.ModelSerializer):
    model = BillsFile
    fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    model = Client
    fields = '__all__'


class ClientOrgsFileSerializer(serializers.ModelSerializer):
    model = ClientOrgsFile
    fields = '__all__'
