from rest_framework import serializers

from .models import Bill, BillsFile, Client, ClientOrgsFile, Organization


class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'


class BillsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillsFile
        fields = '__all__'


class ClientSerializer(serializers.Serializer):
    name = serializers.CharField()
    orgs_count = serializers.IntegerField()
    income = serializers.DecimalField(
        max_digits=9,
        decimal_places=2,
    )


class ClientOrgsFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientOrgsFile
        fields = '__all__'
