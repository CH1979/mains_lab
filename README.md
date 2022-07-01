## Тестовое задание на вакансию Python developer для команды Мэйнс Лаб
---
Для запуска
* Клонировать репозиторий командой:

`git clone https://github.com/CH1979/fabrique-sender`
* Сoздать в директории с репозиторием файл:

`django_secret_key.txt`

cодержащий secret key для django.
* Запустить docker-контейнеры командой:
`docker-compose up -d --build`

### Endpoints

> 1. эндпоинт загрузки файлов bills.xlsx и client_org.xlsx  (может быть по одному на файл, как посчитаете правильным)

* http://127.0.0.1:1337/api/v1/clients/upload/
* http://127.0.0.1:1337/api/v1/bills/upload/

> 2. эндпоинт со списком клиентов

* http://127.0.0.1:1337/api/v1/clients/

> 3. эндпоинт со списком счетов с возможностью фильтровать по организации, клиенту.

* http://127.0.0.1:1337/api/v1/bills/

## Дополнительно

Dict для "классификатора услуг" вынесен в settings.py

Запустить тесты можно командой:

`docker-compose run web python -m pytest`

Документация по API (Swagger) доступна по адресу: http://127.0.0.1:1337/docs/

Мониторинг задач Celery (Flower) доступен по адресу: http://127.0.0.1:5555/
