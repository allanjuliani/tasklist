build:
	@docker-compose build

up:
	@docker-compose up -d

stop:
	@docker-compose down

restart:
	@make stop
	@make up

rebuild:
	@docker-compose down --remove-orphans
	@docker-compose build --no-cache

tasklist-remove:
	@docker-compose down --volumes --remove-orphans

tasklist-clean:
	@make stop
	@docker image rm django_tasklist

docker-clean:
	@make stop
	@docker system prune -a
	@docker volume prune

tests:
	@docker exec -it django_tasklist python manage.py test --settings=tasklist.settings_test

createsuperuser:
	@docker exec -it django_tasklist python manage.py createsuperuser

createtoken:
	@docker exec -it django_tasklist python manage.py drf_create_token $(username)

shell-django:
	@docker exec -it django_tasklist /bin/bash

shell-mysql:
	@docker exec -it mysql_tasklist /bin/bash

shell-nginx:
	@docker exec -it nginx_tasklist /bin/bash
