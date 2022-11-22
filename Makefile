nope:
	$(error Invalid target)

check-env-%:
	@ if [ "${${*}}" = "" ]; then \
		echo "Environment variable $* not set"; \
		exit 1; \
	fi

build:
	docker compose run frontend npm install
	docker compose up --build

shell:
	docker compose exec backend ./manage.py shell

test:
	docker compose run backend ./manage.py test

admin:
	docker compose run backend ./manage.py createsuperuser

fixtures:
	docker compose run backend ./manage.py fixtures
