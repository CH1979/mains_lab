### Тестовое задание на вакансию Python developer для Команды Мэйнс Лаб "
---
Для запуска
* Клонировать репозиторий командой:

`git clone https://github.com/CH1979/fabrique-sender`
* Сoздать в директории с репозиторием файл:

`django_secret_key.txt`

cодержащий secret key для django.
* Запустить docker-контейнеры командой:
`docker-compose up -d --build`


TODO:

API будет доступно по адресу: http://127.0.0.1:1337/api/v1/

Документация API: http://127.0.0.1:1337/docs/

Мониторинг задач Celery (Flower) по адресу: http://127.0.0.1:5555/

Запустить тесты можно командой:

`docker-compose run web python -m pytest`
