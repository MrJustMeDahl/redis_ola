from redis.cluster import RedisCluster, ClusterNode
from redis.exceptions import RedisError

nodes = [
    ClusterNode(host="redis-node-1", port=6379),
    ClusterNode(host="redis-node-2", port=6379),
    ClusterNode(host="redis-node-3", port=6379),
]

def getRedisCluster():
    return RedisCluster(startup_nodes=nodes, decode_responses=True)

def createUser(userId, userName, userEmail):
    redisCluster = getRedisCluster()
    try:
        if redisCluster.exists(userId):
            print(f"User {userId} already exists.")
            return None
        redisCluster.hset(userId, mapping={"name": userName, "email": userEmail})
        print(f"User {userId} created successfully.")
        return redisCluster.hgetall(userId)
    except RedisError as e:
        print(f"Error creating user {userId}: {e}")
        return None

def getUser(userId):
    redisCluster = getRedisCluster()
    try:
        user = redisCluster.hgetall(userId)
        if not user:
            print(f"User {userId} not found.")
            return None
        return user
    except RedisError as e:
        print(f"Error retrieving user {userId}: {e}")
        return None

def updateUser(userId, userName=None, userEmail=None):
    redisCluster = getRedisCluster()
    try:
        if not redisCluster.exists(userId):
            print(f"User {userId} not found.")
            return None
        if userName:
            redisCluster.hset(userId, "name", userName)
        if userEmail:
            redisCluster.hset(userId, "email", userEmail)
        return redisCluster.hgetall(userId)
    except RedisError as e:
        print(f"Error updating user {userId}: {e}")
        return None

def deleteUser(userId):
    redisCluster = getRedisCluster()
    try:
        if not redisCluster.exists(userId):
            print(f"User {userId} not found.")
            return None
        result = redisCluster.delete(userId)
        if result == 1:
            print(f"User {userId} deleted successfully.")
            return True
        else:
            print(f"Failed to delete user {userId}.")
            return False
    except RedisError as e:
        print(f"Error deleting user {userId}: {e}")
        return None