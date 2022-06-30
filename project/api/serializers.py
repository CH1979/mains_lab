from rest_framework import serializers

from .models import Bill, BillsFile, Client, ClientOrgsFile


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class BillsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillsFile
        fields = '__all__'


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = '__all__'


class ClientOrgsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOrgsFile
        fields = '__all__'
