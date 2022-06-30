import random
from string import whitespace
from typing import Dict

from django.conf import settings


def detect_fraud(service: str) -> float:
    return random.random()

def classify_service(service: str) -> Dict:
    service_class = random.choice(
        list(settings.SERVICE_CLASSES.keys())
    )
    service_name = settings.SERVICE_CLASSES[service_class]
    service = {
        'service_class': service_class,
        'service_name': service_name
    }
    return service

def preprocess_address(address: str) -> str:
    if (address in whitespace) or (address == '-'):
        return ''
    else:
        return 'Адрес: {}'.format(address)
