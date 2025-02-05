migrate:
	docker compose run --rm backend python manage.py migrate $(app)

migrations:
	docker compose run --rm backend python manage.py makemigrations $(app)

superuser:
	docker compose run --rm backend python manage.py createsuperuser

show_urls:
	docker compose run --rm backend python manage.py show_urls