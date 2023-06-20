APP_CONTAINER_NAME = "crud-auth-github"

## Docker
.PHONY: exec-bash
exec-bash:
	docker exec -it $(APP_CONTAINER_NAME) bash ${ARGS}
migrate:
	docker compose exec -it $(APP_CONTAINER_NAME) python manage.py migrate

createsuperuser:
	docker compose exec -it $(APP_CONTAINER_NAME) python manage.py createsuperuser


clean-pers-data:
	rm -rf ./data/db