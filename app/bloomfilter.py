import redis

redisClient = redis.StrictRedis(host='localhost', port=6379, db=0)
filter_name = 'userfilter'

def check_user(user_id):
    result = redisClient.execute_command('BF.EXISTS', filter_name,user_id)
    if result == 1:
        print(f"User {user_id} exists in the Bloom Filter (probable).")
    else:
        print(f"User {user_id} does not exist in the Bloom Filter.")

def check_false_positive(user_id):
    result = redisClient.execute_command('BF.EXISTS', filter_name,user_id)
    if result == 1:
        print(f"User {user_id} exists in the Bloom Filter (probable).")
    else:
        print(f"User {user_id} does not exist in the Bloom Filter.")
    return result