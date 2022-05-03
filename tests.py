for i in range(3):
    files = open("detected.txt", "w+")
    user = input("word... ")
    files.write(user)
    files.close()
    