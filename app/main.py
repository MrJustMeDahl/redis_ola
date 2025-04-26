from crud import createUser, getUser, updateUser, deleteUser

def main():
    createUser("user1", "John Doe", "johnd@test.com")
    createUser("user2", "Jane Doe", "janed@test.com")
    print(getUser("user1"))
    updateUser("user1", userName="John Smith", userEmail="johns@test.com")
    print(getUser("user1"))
    deleteUser("user1")
    print(getUser("user1"))

if __name__ == "__main__":
    main()