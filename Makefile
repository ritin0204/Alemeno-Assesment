all: runserver

.PHONY: tests
test:
	python manage.py test

.PHONY: makemigrations
makemigrations:
	python manage.py makemigrations

.PHONY: migrate
migrate:
	python manage.py migrate

.PHONY: load_data
load-data:
	python manage.py import_data

.PHONY: runserver
runserver:
	python manage.py runserver 0.0.0.0:8000

.PHONY: initial-setup
initial-setup:
	make makemigrations
	make migrate
	make load-data
