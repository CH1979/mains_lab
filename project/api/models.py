import celery
from django.db import models
from django.dispatch import receiver

from .validators import validate_upload_file


class ClientOrgsFile(models.Model):
    """Client-organization file model"""
    name = models.FileField(
        upload_to='clients/',
        validators=[validate_upload_file],
    )
    
    def __str__(self):
        return self.name


@receiver(models.signals.post_save, sender=ClientOrgsFile)
def run_clients_file_preprocessing(sender, instance, created, *args, **kwargs):
    """Run Celery task for preprocessing ClientOrgs file"""
    if created:
        celery.current_app.send_task(
            'api.tasks.read_client_org_file',
            (instance.pk, )
        )


class BillsFile(models.Model):
    """Bills file model"""
    name = models.FileField(
        upload_to='bills/',
        validators=[validate_upload_file],
    )


@receiver(models.signals.post_save, sender=BillsFile)
def run_bills_file_preprocessing(sender, instance, created, *args, **kwargs):
    """Run Celery task for preprocessing Bills file"""
    if created:
        celery.current_app.send_task(
            'api.tasks.read_bills_file',
            (instance.pk, )
        )


class Client(models.Model):
    """Client model"""
    name = models.CharField(
        max_length=50,
        unique=True,
    )

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return self.name


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

    def __str__(self) -> str:
        return '{} - {} № {} - {}'.format(
            self.client,
            self.organization,
            self.number,
            self.bill_sum
        )
