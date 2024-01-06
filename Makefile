up:
	@docker-compose up --build -d

down:
	@docker-compose down

sh:
	@docker exec -it library-svc sh

mkmigrations:
	@docker exec -i library-svc python src/manage.py makemigrations

migrate:
	@docker exec -i library-svc python src/manage.py migrate

dj-shell:
	@docker exec -it library-svc python src/manage.py shell

test:
	@docker exec -it library-svc pytest src/apps -s -p no:warnings
