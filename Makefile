migrate:
	docker compose exec -it backend python manage.py migrate $(app)

migrations:
	docker compose exec -it backend python manage.py makemigrations $(app)

superuser:
		docker compose exec -it backend python manage.py createsuperuser