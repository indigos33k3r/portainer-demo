from fabric.api import task, local

@task
def down():
    local('docker-compose down')
    local('rm -rf /tmp/manager_run')

@task
def up():
    local('docker-compose up -d manager1 manager2 worker1 worker2')
    local('docker-compose exec manager1 docker swarm init')
    token_worker = local('docker-compose exec manager1 docker swarm join-token -q worker', capture=True)
    token_manager = local('docker-compose exec manager1 docker swarm join-token -q manager', capture=True)
    local('docker-compose exec manager2 docker swarm join --token {} manager1:2377'.format(token_manager))
    local('docker-compose exec worker1 docker swarm join --token {} manager1:2377'.format(token_worker))
    local('docker-compose exec worker2 docker swarm join --token {} manager1:2377'.format(token_worker))
    local('docker-compose up -d proxy templates portainer')

@task
def demo():
    down()
    up()
