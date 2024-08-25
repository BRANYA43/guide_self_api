# Docker
install-docker:
	curl -fsSL https://get.docker.com -o get-docker.sh; sudo sh ./get-docker.sh; rm get-docker.sh

up:
	sudo docker compose up $(f)

down:
	sudo docker compose down $(f)

reup: down up

container-prune:
	sudo docker container prune -f

image-prune:
	sudo docker image prune -af

volume-prune:
	sudo docker volume prune -af

network-prune:
	sudo docker network prune -f

prune-all: container-prune image-prune volume-prune network-prune

ps:
	sudo docker ps -a

images:
	sudo docker images

shell-api:
	sudo docker exec -it api /bin/bash

shell-db:
	sudo docker exec -it db /bin/bash

shell-nginx:
	sudo docker exec -it nginx /bin/bash

logs-api:
	sudo docker logs $(f) api

logs-db:
	sudo docker logs $(f) db

logs-nginx:
	sudo docker logs $(f) nginx
