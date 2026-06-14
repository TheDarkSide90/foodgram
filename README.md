## Foodgram - сборник рецептов от людей.

## Автор: Васильев Никита Романович
[Телеграмм](https://t.me/TheDarkSide90).

## Примененный стек технологий:
- Python 3.12
- Django
- Django REST Framework (DRF)
- django-filter
- PostgreSQL
- Gunicorn
- Nginx
- Docker

## Развёртывание проекта:
```bash
git clone https://github.com/TheDarkSide90/foodgram.git
```
```bash
cd foodgram
```
```bash
sudo docker compose pull
```
```bash
sudo docker compose down
```
```bash
sudo docker compose up -d
```
```bash
sudo docker compose exec backend python manage.py makemigrations users --noinput
```
```bash
sudo docker compose exec backend python manage.py makemigrations --noinput
```
```bash
sudo docker compose exec backend python manage.py migrate --noinput
```
```bash
sudo docker compose exec backend python manage.py collectstatic --noinput
```
```bash
sudo docker compose exec backend cp -r /app/staticfiles/. /static/
```
## Вход в админку:
```bash
sudo docker compose exec backend python manage.py createsuperuser
```
- email: test@test.com
- first_name: test
- last_name: test
- password: test

## Доменное имя проекта:
https://foodgramproject.mooo.com/
