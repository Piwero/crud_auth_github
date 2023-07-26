APP_CONTAINER_NAME = "crud-auth-github"

# Docker
## Main app
.PHONY: exec-bash
exec-bash:
	docker exec -it $(APP_CONTAINER_NAME) bash ${ARGS}
migrate:
	docker compose exec -it $(APP_CONTAINER_NAME) python manage.py migrate
createsuperuser:
	docker compose exec -it $(APP_CONTAINER_NAME) python manage.py createsuperuser
collectstatic:
		docker compose exec -it $(APP_CONTAINER_NAME) python manage.py collectstatic
test:
	docker compose exec -it $(APP_CONTAINER_NAME) pytest
shell:
	docker compose exec -it $(APP_CONTAINER_NAME) python manage.py shell_plus

clean-pers-data:
	rm -rf ./data/db

## DB
exec-db:
	docker exec -it postgres_db psql -U postgres