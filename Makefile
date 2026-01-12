.PHONY: up runserver migrate makemigrations stop logs shell


up:
	docker compose up --build -d


runserver:
	docker compose run --rm web python manage.py runserver 0.0.0.0:8000


makemigrations:
	docker compose run --rm web python manage.py makemigrations


migrate:
	docker compose run --rm web python manage.py migrate


logs:
	docker compose logs -f web


shell:
	docker compose run --rm web python manage.py shell


stop:
	docker compose down