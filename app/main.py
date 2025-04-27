from crud import createUser, getUser, updateUser, deleteUser
from bloomfilter import check_user, check_false_positive

def main():
    """     
    createUser("user1", "John Doe", "johnd@test.com")
    createUser("user2", "Jane Doe", "janed@test.com")
    print(getUser("user1"))
    updateUser("user1", userName="John Smith", userEmail="johns@test.com")
    print(getUser("user1"))
    deleteUser("user1")
    print(getUser("user1"))
    """
    
    check_user("user1")
    check_user("user7")

    baseid = 'user'
    startid = 26

    while True:
        user_id = f"{baseid}{startid}"
        result = check_false_positive(user_id)
        startid += 1
        if result == 1:
            break

if __name__ == "__main__":
    main()