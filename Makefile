define USAGE
Commands:
	make app					Up application and database infrastructure
	make app-logs				Follow the logs in app container
	flake8						flake8
endef


.PHONY: app
app:
	docker compose -f docker-compose.yml  up --build -d

.PHONY: app-logs
app-logs:
	docker logs main-app -f

.PHONY: flake8
flake8:
	docker-compose run --rm app sh -c "flake8"
