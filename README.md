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
cd foodgram
sudo docker compose pull
sudo docker compose down
sudo docker compose up -d
sudo docker compose exec backend python manage.py makemigrations users --noinput
sudo docker compose exec backend python manage.py makemigrations --noinput
sudo docker compose exec backend python manage.py migrate --noinput
sudo docker compose exec backend python manage.py collectstatic --noinput
sudo docker compose exec backend cp -r /app/staticfiles/. /static/
```
## Вход в админку:
sudo docker compose exec backend python manage.py createsuperuser
email: test@test.com
first_name: test
last_name: test
password: test

## Доменное имя проекта:
https://foodgramproject.mooo.com/
