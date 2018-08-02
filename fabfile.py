from fabric.api import task, local

@task
def down():
    local('/usr/local/bin/docker-compose down')
    local('rm -rf /tmp/manager_run')

@task
def up():
    local('/usr/local/bin/docker-compose up -d manager1 manager2 worker1 worker2')
    local('/usr/local/bin/docker-compose exec -T manager1 docker swarm init')
    token_worker = local('/usr/local/bin/docker-compose exec -T manager1 docker swarm join-token -q worker', capture=True)
    token_manager = local('/usr/local/bin/docker-compose exec -T manager1 docker swarm join-token -q manager', capture=True)
    local('/usr/local/bin/docker-compose exec -T manager2 docker swarm join --token {} manager1:2377'.format(token_manager))
    local('/usr/local/bin/docker-compose exec -T worker1 docker swarm join --token {} manager1:2377'.format(token_worker))
    local('/usr/local/bin/docker-compose exec -T worker2 docker swarm join --token {} manager1:2377'.format(token_worker))
    local('/usr/local/bin/docker-compose up -d proxy portainer')

@task
def demo():
    down()
    up()
