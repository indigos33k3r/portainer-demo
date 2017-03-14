#!/bin/bash

# Fresh start
docker-compose down

# Up all dinds nodes
docker-compose up -d manager1 manager2 worker1 worker2

# Manager1 init
docker-compose exec manager1 docker swarm init
TOKEN_WORKER="$(docker-compose exec manager1 docker swarm join-token -q worker)"
TOKEN_MANAGER=`docker-compose exec manager1 docker swarm join-token manager | grep 'token' | xargs | sed -e 's/--token //'`

Manager2 join
docker-compose exec manager2 docker swarm join --token $TOKEN_MANAGER manager1:2377

Worker1 join
docker-compose exec worker1 docker swarm join --token $TOKEN_WORKER manager1:2377

# Worker2 join
docker-compose exec worker2 docker swarm join --token $TOKEN_WORKER manager1:2377

# Up portainer
docker-compose up -d proxy templates portainer
