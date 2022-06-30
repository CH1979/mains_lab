import pandas as pd

from core.celery import app
from .models import Bill, BillsFile, Client, ClientOrgsFile, Organization
from .utils import classify_service, detect_fraud, preprocess_address


@app.shared_task
def read_client_org_file(pk):
    filename = ClientOrgsFile.objects.get(pk=pk).get('name')

    clients = pd.read_excel(filename, sheet_name='client')
    organizations = pd.read_excel(filename, sheet_name='organization')

    objs = []
    for client_name in clients['name'].values:
        objs.append(Client(name=client_name))

    Client.objects.bulk_create(objs, ignore_conflicts=True)

    objs = []
    for row in organizations.iterrows():
        client = Client.objects.get(name=row['client_name'])
        address = preprocess_address(row['address'])

        objs.append(Organization(
            name=row['name'],
            client=client,
            address=address,
            fraud_weight=0
        ))
    Organization.objects.bulk_create(objs, ignore_conflicts=True)


@app.task
def read_bills_file(pk):
    filename = BillsFile.objects.get(pk=pk).get('name')

    bills = pd.read_excel(filename)

    objs = []
    for row in bills.iterrows():
        client = Client.objects.get(name=row['client_name'])
        organization = Organization.objects.get(name=row['client_org'])
        service = classify_service(row['service'])
        fraud_score = detect_fraud(row['service'])

        if fraud_score >= 0.9:
            organization.fraud_weight += 1
            organization.save()

        objs.append(Bill(
            client=client,
            organization=organization,
            number=row['number'],
            bill_sum=row['sum'],
            bill_data=row['date'],
            fraud_score=fraud_score,
            service_class=service['service_class'],
            service_name=service['service_name']
        ))

    Bill.objects.bulk_create(objs, ignore_conflicts=True)
