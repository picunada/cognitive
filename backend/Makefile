nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

# Django
django_migrate:
	./manage.py migrate -v 3 --noinput
	./manage.py makemigrations
	./manage.py migrate -v 3 --noinput

test:
	./manage.py test

collectstatic:
	./manage.py collectstatic --noinput

django: django_migrate
	./manage.py runserver 0.0.0.0:8000

gunicorn: collectstatic django_migrate
	gunicorn \
		--bind 0.0.0.0:8000 \
		--workers 4 \
		project.wsgi:application

