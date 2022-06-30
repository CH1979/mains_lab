from django.conf import settings

from api.utils import (
    classify_service,
    detect_fraud,
    preprocess_address
)

def test_classify_service():
    service = classify_service('вызов врача на дом')

    assert isinstance(service, dict)
    assert service['service_class'] in settings.SERVICE_CLASSES.keys()
    assert service['service_name'] in settings.SERVICE_CLASSES.values()
    assert service['service_name'] == \
        settings.SERVICE_CLASSES[service['service_class']]

def test_detect_fraud():
    fraud_score = detect_fraud('вызов врача на дом')

    assert isinstance(fraud_score, float)
    assert 0 <= fraud_score <= 1

def test_preprocess_address():
    address_before = '117519, г Москва, ул Кировоградская, д 22Б'
    address_after = 'Адрес: 117519, г Москва, ул Кировоградская, д 22Б'

    assert address_after == preprocess_address(address_before)

    address_before = ''
    address_after = ''

    assert address_after == preprocess_address(address_before)

    address_before = ''
    address_after = ''

    assert address_after == preprocess_address(address_before)

    address_before = ' '
    address_after = ''

    assert address_after == preprocess_address(address_before)

    address_before = '-'
    address_after = ''

    assert address_after == preprocess_address(address_before)
