import pandas as pd
import pytest

from api.models import Bill, Client, Organization
from api.tasks import (
    save_bills,
    save_clients,
    save_organizations
)


@pytest.mark.django_db
def test_save_clients():
    df = pd.DataFrame({
        'name': ['client1', 'client2']
    })
    save_clients(df)

    clients = Client.objects.all()
    assert len(clients) == 2

    clients = Client.objects.filter(name='client1')
    assert len(clients) == 1


@pytest.mark.django_db
def test_save_organizations():
    clients_df = pd.DataFrame({
    'name': ['client1', 'client2']
    })
    save_clients(clients_df)

    orgs_df = pd.DataFrame({
        'client_name': ['client1', 'client1', 'client2'],
        'name': ['OOO Client1Org1', 'OOO Client1Org2', 'OOO Client2Org1'],
        'address': [
            '117519, г Москва, ул Кировоградская, д 22Б',
            '119180, Москва г, Полянка М. ул, д.7/7, стр.1',
            '142802, Московская обл, Ступинский р-н, Ступино г, Андропова ул, д.64'
        ]
    })
    save_organizations(orgs_df)

    orgs = Organization.objects.all()
    assert len(orgs) == 3

    orgs = Organization.objects.filter(client__name='client1')
    assert len(orgs) == 2

    orgs = Organization.objects.filter(name='OOO Client2Org1')
    assert len(orgs) == 1


@pytest.mark.django_db
def test_save_bills_failure():
    df = pd.DataFrame({
        'client_name': ['client1', 'client2'],
        'client_org': ['OOO Client1Org1', 'OOO Client2Org1'],
        '№': [1, 1],
        'sum': [10000, 3333],
        'date': ['2022-01-01', '2022-02-01'],
        'service': ['вызов врача на дом', 'забор биоматериала']
    })
    save_bills(df)
    
    bills = Bill.objects.all()

    assert len(bills) == 0


@pytest.mark.django_db
def test_save_bills_success():
    clients_df = pd.DataFrame({
    'name': ['client1', 'client2']
    })
    save_clients(clients_df)

    orgs_df = pd.DataFrame({
        'client_name': ['client1', 'client1', 'client2'],
        'name': ['OOO Client1Org1', 'OOO Client1Org2', 'OOO Client2Org1'],
        'address': [
            '117519, г Москва, ул Кировоградская, д 22Б',
            '119180, Москва г, Полянка М. ул, д.7/7, стр.1',
            '142802, Московская обл, Ступинский р-н, Ступино г, Андропова ул, д.64'
        ]
    })
    save_organizations(orgs_df)

    bills_df = pd.DataFrame({
        'client_name': ['client1', 'client2'],
        'client_org': ['OOO Client1Org1', 'OOO Client2Org1'],
        '№': [1, 1],
        'sum': [10000, 3333],
        'date': ['2022-01-01', '2022-02-01'],
        'service': ['вызов врача на дом', 'забор биоматериала']
    })
    save_bills(bills_df)
    
    bills = Bill.objects.all()

    assert len(bills) == 2
