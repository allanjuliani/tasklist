PORT=8000
SITE=tasklist

start_br:
	@./manage.py runserver 0.0.0.0:$(PORT) --settings=$(SITE).settings_pt_br &

start:
	@./manage.py runserver 0.0.0.0:$(PORT) --settings=$(SITE).settings &>/dev/null &

translate_br:
	@./manage.py makemessages -l pt_BR
	@./manage.py compilemessages -l pt_BR

test:
	@./manage.py test

migrate:
	@./manage.py makemigrations
	@./manage.py migrate

stop:
	@pkill -f $(PORT)
