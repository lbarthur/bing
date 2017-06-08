f = open("/reboot/user.txt", "a+")
username=""
password=""
while True:
    username=input("please input your username(quit):").strip()
    password = input("please input your password:").strip()
    repass = input("please confirm your password:").strip()
    if username =="":
        print ("user name is null, please register again ")
        continue

    elif password =="":
        print ("password is null, please register again ")
        continue

    elif repass =="" or repass != password:
        print ("password is not same,please register again")
        continue
    else :
        print ("Congratulation !~")
        break



f.write("%s:%s\n" %(username,password))
f.close()