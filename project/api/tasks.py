"""
Celery tasks
"""
import logging
import re
from typing import Optional

from celery import shared_task
import pandas as pd

from .exceptions import (
    DateValueError,
    NumberValueError,
    ServiceValueError,
    SumValueError
)
from .models import (
    Bill,
    BillsFile,
    Client,
    ClientOrgsFile,
    Organization,
    Schema
)
from .utils import classify_service, detect_fraud, preprocess_address


logger = logging.getLogger(__name__)


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


def get_client(name: str, filename: str, idx: int) -> Optional[Client]:
    """Get client instance"""
    try:
        client = Client.objects.get(name=name)
    except Client.DoesNotExist:
        logger.error(
            'Unknown Client in file {} row {}'.format(filename, idx)
        )
        client = None
    return client


def get_organization(name: str, filename: str, idx: int) \
    -> Optional[Organization]:
    """Get organization instance"""
    try:
        organization = Organization.objects.get(
            name=name
        )
    except Organization.DoesNotExist:
        logger.error(
            'Unknown Organization in file {} row {}'.format(filename, idx)
        )
        organization = None
    return organization


def check_service(service: str, filename: str, idx: int) -> None:
    """Check service is not empty"""
    if re.fullmatch(r'[\s\-]+', service) is not None:
        logger.error(
            'Empty value in service description in ' \
            'file {} row {}'.format(filename, idx)
        )
        raise ServiceValueError


def save_bills(bills: pd.DataFrame, filename: str, schema: Schema) -> None:
    """Save bills"""
    objs = []
    for idx, row in bills.iterrows():
        client = get_client(row[schema.client_field_name], filename, idx)
        if client is None:
            continue

        organization = get_organization(row[schema.org_field_name], filename, idx)
        if organization is None:
            continue

        service_description = row[schema.service_field_name]

        check_service(service_description, filename, idx)

        try:
            bill_number = int(row[schema.number_field_name])
        except ValueError:
            logger.error(
                'Incorrect value in bill number in ' \
                'file {} row {}'.format(filename, idx)
            )
            raise NumberValueError

        try:
            bill_sum = float(row[schema.sum_field_name])
        except ValueError:
            logger.error(
                'Incorrect value in bill sum in ' \
                'file {} row {}'.format(filename, idx)
            )
            raise SumValueError


        service = classify_service(service_description)
        fraud_score = detect_fraud(service_description)

        if fraud_score >= 0.9:
            organization.fraud_weight += 1
            organization.save()

        objs.append(Bill(
            client=client,
            organization=organization,
            number=bill_number,
            bill_sum=bill_sum,
            bill_date=row[schema.date_field_name],
            fraud_score=fraud_score,
            service_class=service['service_class'],
            service_name=service['service_name']
        ))

    Bill.objects.bulk_create(objs, ignore_conflicts=True)


def get_schema_id(columns):
    """Get fields schema"""
    schemas = Schema.objects.values_list(
        'id',
        'client_field_name',
        'org_field_name',
        'number_field_name',
        'sum_field_name',
        'date_field_name',
        'service_field_name'
    )
    for schema in schemas:
        if set(schema[1:]) == set(columns):
            return schema[0]
    return None


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
    schema_id = get_schema_id(bills.columns)
    schema = Schema.objects.get(pk=schema_id)
    save_bills(bills, filename, schema)
