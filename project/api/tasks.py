"""
Celery tasks
"""
from celery import shared_task
import pandas as pd

from .models import Bill, BillsFile, Client, ClientOrgsFile, Organization
from .utils import classify_service, detect_fraud, preprocess_address


def save_clients(clients: pd.DataFrame) -> None:
    """Save clients"""
    objs = []
    for client_name in clients['name'].values:
        objs.append(Client(name=client_name))

    Client.objects.bulk_create(objs, ignore_conflicts=True)


def save_organizations(organizations: pd.DataFrame) -> None:
    """Save organizations"""
    objs = []
    for _, row in organizations.iterrows():
        client = Client.objects.get(name=row['client_name'])
        address = preprocess_address(row['address'])

        objs.append(Organization(
            name=row['name'],
            client=client,
            address=address,
            fraud_weight=0
        ))
    Organization.objects.bulk_create(objs, ignore_conflicts=True)


def save_bills(bills: pd.DataFrame) -> None:
    """Save bills"""
    objs = []
    for _, row in bills.iterrows():
        try:
            client = Client.objects.get(name=row['client_name'])
        except Client.DoesNotExist:
            break

        try:
            organization = Organization.objects.get(name=row['client_org'])
        except Organization.DoesNotExist:
            break

        service = classify_service(row['service'])
        fraud_score = detect_fraud(row['service'])

        if fraud_score >= 0.9:
            organization.fraud_weight += 1
            organization.save()

        objs.append(Bill(
            client=client,
            organization=organization,
            number=row['№'],
            bill_sum=row['sum'],
            bill_date=row['date'],
            fraud_score=fraud_score,
            service_class=service['service_class'],
            service_name=service['service_name']
        ))

    Bill.objects.bulk_create(objs, ignore_conflicts=True)


@shared_task
def read_client_org_file(pk):
    """Preprocess ClientOrg file"""
    filename = ClientOrgsFile.objects.get(pk=pk).name

    clients = pd.read_excel(filename, sheet_name='client')
    organizations = pd.read_excel(filename, sheet_name='organization')

    save_clients(clients)
    save_organizations(organizations)


@shared_task
def read_bills_file(pk):
    """Preprocess Bills file"""
    filename = BillsFile.objects.get(pk=pk).name

    bills = pd.read_excel(filename)
    save_bills(bills)
