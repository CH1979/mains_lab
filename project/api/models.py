from django.db import models


class ClientOrgsFile(models.Model):
    """Client-organization file model"""
    name = models.FileField(
        upload_to='clients',
    )


class BillsFile(models.Model):
    """Bills file model"""
    name = models.FileField(
        upload_to='bills',
    )


class Client(models.Model):
    """Client model"""
    name = models.CharField(
        max_length=50,
        unique=True,
    )


class Organization(models.Model):
    """Organizaton model"""
    name = models.CharField(
        max_length=50,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    address = models.CharField(
        max_length=250,
    )
    fraud_weight = models.IntegerField(
        default=0
    )

    class Meta:
        unique_together = [['name', 'client']]


class Bill(models.Model):
    """Bill model"""
    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )
    number = models.IntegerField()
    bill_sum = models.DecimalField(
        max_digits=9,
        decimal_places=2,
    )
    bill_date = models.DateField()
    service = models.TextField()
    fraud_score = models.FloatField()
    service_class = models.IntegerField()
    service_name = models.CharField(
        max_length=20
    )

    class Meta:
        unique_together = [['organization', 'number']]
