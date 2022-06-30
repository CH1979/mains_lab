from typing import Dict


SERVICE_CLASSES = {
    1: 'консультация',
    2: 'лечение',
    3: 'стационар',
    4: 'диагностика',
    5: 'лаборатория'
}


def detect_fraud(service: str) -> float:
    pass

def classify_service(service: str) -> Dict:
    pass

def preprocess_address(address: str) -> str:
    pass
