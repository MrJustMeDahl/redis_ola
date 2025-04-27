## Redis OLA

We were tasked with implementing 2 of the following 6 projects:

1. Redis with Retention Policy in Redis

2. Redis Master-Slave Replication

3. Redis Cluster

4. Redis Security

5. Redis Publish-Subscribe Pattern

6. Redis Bloom Filters

Tasks are specified here: https://github.com/MrJustMeDahl/redis_ola/blob/main/Redis%20Study%20point%20Assignment.pdf

Besides that we are to develop a small application that will make use of one of the redis implementations as well as being able to perform all CRUD operations up against Redis.

### 3. Redis Cluster

For this assignment we are simulating the cluster nodes being on different machines by running each node in a separate docker container. To allow the python application to connect to the Redis cluster, we are also running the application within a docker container on the same docker network as the cluster. (This is necessary because all the nodes are located on the same machine, therefore making use of the internal docker DNS to direct traffic, which the python application does not have access to, if it is not part of the same docker network)

#### 3.1 Install Redis on several machines and configure them to run on different ports.

This setup is handled through the docker compose file, which hold the formula to creating all the containers on different ports (7001, 7002, 7003) and have them configured to be ready for creating a cluster, by passing the redis.conf file to the containers through the volumes tag in the docker-compose file. The compose file also handles passing the command to start the redis server.

```yml
version: "3"

services:
  redis-node-1:
    image: redis:7
    container_name: redis-node-1
    ports:
      - "7001:6379"
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      redis-cluster:
        ipv4_address: 172.30.0.2

  redis-node-2:
    image: redis:7
    container_name: redis-node-2
    ports:
      - "7002:6379"
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      redis-cluster:
        ipv4_address: 172.30.0.3

  redis-node-3:
    image: redis:7
    container_name: redis-node-3
    ports:
      - "7003:6379"
    volumes:
      - ./redis.conf:/usr/local/etc/redis/redis.conf
    command: ["redis-server", "/usr/local/etc/redis/redis.conf"]
    networks:
      redis-cluster:
        ipv4_address: 172.30.0.4

  python-app:
    build:
      context: ..
      dockerfile: Dockerfile
    container_name: python-app
    volumes:
      - ../app:/app
    working_dir: /app
    command: ["tail", "-f", "/dev/null"]
    networks:
      redis-cluster:
        ipv4_address: 172.30.0.5
    depends_on:
      - redis-node-1
      - redis-node-2
      - redis-node-3

networks:
  redis-cluster:
    driver: bridge
    ipam:
      config:
        - subnet: 172.30.0.0/16

```

#### 3.2 Use the Redis CLI or Redis Telnet CLI to set up a Redis Cluster configuration.
The configuration file passed to each node defines that the nodes are ready for a cluster to be created.

```
port 6379
cluster-enabled yes
cluster-config-file nodes.conf
cluster-node-timeout 5000
appendonly yes
```

In order to create the cluster using the redis cli, it is in this case required to create a temporary docker container using the redis image on the same network as the nodes, as we need to define the IP addresses of the nodes, and therefore must have access to the internal docker IPs.

The following command will create the cluster, and must be run after the nodes are running, but before the application can run, because the nodes need to be online for the command to handle the handshake between the nodes when creating the cluster, and the application can't connect to the cluster before it has been created. 

```
docker run -it --rm --network redis-cluster_redis-cluster redis:7 redis-cli --cluster create 172.30.0.2:6379 172.30.0.3:6379 172.30.0.4:6379 --cluster-replicas 0
```

The command starts a redis container on the same network and uses the redis-cli to create the cluster based on the docker IPs of the nodes. In this case we chose to have 0 replicas to minimize the amount of containers running on the same machine, although in a production environment it is recommended to make a cluster of at least 6 nodes, 3 being master nodes and 3 being replicas, to ensure fault safety, as a replica node would take over in case a master node fails. 

![image](documentation\cluster_creation.png)

#### 3.3 Use the Redis CLI or Redis Telnet CLI to store user data in the Redis Cluster.

When accessing the Redis Cluster through the Redis CLI it is important to remember using the -c tag. Basically one is able to connect to the cluster through any of the nodes, however without the -c tag, you'd only have access to the data in the specific node. Meaning if you were to add new data it would always be stored on the node you connected to, even though it was supposed to be redirected to another node. 

```
docker exec -it redis-node-1 redis-cli -c
```
Inside the Redis CLI the following commands were used to add users to the cluster.
```
HSET user3 name "Alice Smith" email "alice@example.com"
HSET user4 name "Bob Johnson" email "bob@example.com"
HSET user5 name "Charlie Lee" email "charlie@example.com"
HSET user6 name "Diana Prince" email "diana@example.com"
HSET user7 name "Evan Wright" email "evan@example.com"
```

#### 3.4 Verify that data is distributed evenly across the Redis Cluster. 

![image](documentation\redis_cli_users_added.png)

When adding the users to the cluster, Redis redirects the data to the correct node based the hash slot of the data. The image indicates that Redis is allocating hash slots and distributing data to all 3 nodes.

#### 3.5 Test the configuration by stopping one of the Redis instances and verifying that the Redis Cluster can handle requests. 

