run:
	gunicorn -c gunicorn_conf.py "app:create_app()"

psql:
	psql -U postgres -h localhost -p 5432 -d medsync

install:
	pip install -r requirements.txt

uninstall:
	pip uninstall -r requirements.txt

redis:
	docker exec -it redis_medsync redis-cli

test:
	pytest -v -p no:warnings

cloc:
	cloc --exclude-dir=venv,migrations .

tree:
	tree -I 'venv|migrations|__pycache__' .

celery:
	celery -A app.settings.tasks worker --loglevel=INFO