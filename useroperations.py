import pickle

def registeuser(username,password):
    users={username:password}
    f = open("userbin","wb")
    pickle.dump(users,f)
    f.close()


def deleteuser(username):
    content={}
    f = open("userbin","rb")
    content=pickle.load(f)
    f.close()
    content.pop(username)
    f = open("userbin", "wb")
    pickle.dump(content, f)
    f.close()

def modifyuser():
    content={}
    f = open("userbin", "rb")
    content=pickle.load(f)
    f.close()
    content['bing']='bing123'
    f = open("userbin", "wb")
    pickle.dump(content, f)
    f.close()

def showalluser():
    content={}
    f = open("userbin", "rb")
    content=pickle.load(f)
    f.close()
    print (content)

adduser()
deluser()
modifyuser()
searchuser()



