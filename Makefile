nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

up:
	docker compose run frontend npm install
	docker compose up -d --build

shell:
	docker compose exec app ./manage.py shell

test:
	docker compose run app ./manage.py test

admin:
	docker compose run app ./manage.py createsuperuser

fixtures:
	docker compose run app ./manage.py fixtures
