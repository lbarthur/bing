from flask import Flask, request, render_template,redirect,session
import pymysql as mysql
import datetime
import traceback
import json


connect = mysql.Connect(
    host='localhost',
    port=3306,
    user='root',
    passwd='lb1390',
    db='Bing',
    charset='utf8'
)
connect.autocommit(True)
cur = connect.cursor()

app=Flask(__name__)
app.secret_key="my first flask app"
#GET
@app.route('/userlist')
def listuser():
    #判断用户是否登录状态，没有的话 跳转到登录界面
    if not session.get('name',None):
        return redirect('/login')
    users=[]
    fields=['id','name','email','mobile','create_time','last_time']
    sql = 'select %s from users' % ','.join(fields)
    cur.execute(sql)
    result = cur.fetchall()
    for line in result:
        user = dict((k, line[i]) for i, k in enumerate(fields))
        users.append(user)

    return render_template("userlist.html",users=users)

#GET
@app.route('/userinfo')
def userinfo():
    if not session.get('name',None):
        return redirect('/login')
    username = request.args.get('name')
    fields = ['id', 'name', 'email', 'mobile', 'create_time', 'last_time']
    sql = 'select %s from users WHERE name=%s' % (','.join(fields),username)
    cur.execute(sql)
    result = cur.fetchone()
    user = dict((k, result[i]) for i, k in enumerate(fields))
    return render_template("userinfo.html", user=user)

#POST
@app.route('/register',methods=['GET','POST'])
def register():
    if not session.get('name',None):
        return redirect('/login')
    currentdate = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        #从前端form获取值,并存入字典中
        register_info = dict(request.form)
        #register_info={'name': ['123'], 'password': ['123'], 'repwd': ['123'], 'email': ['123@123.com'], 'mobile': ['123123123'], 'role': ['admin'], 'status': ['0']}
        #给register_info手动加入2列，因为表单中并没有lasttime和createtime的值
        register_info['create_time']=[currentdate]
        register_info['last_time'] = [currentdate]

        username = register_info.get('name', None)[0]
        role =register_info.get('role',None)[0]
        password =register_info.get('password',None)[0]
        repwd = register_info.get('repwd',None)[0]
        #要插入的列名
        fields=['name', 'password' , 'email', 'mobile', 'role','status','create_time','last_time']
        #要插入的值  列表生成式，字典转list。 并且去除不想要的值repwd
        #['234', '123', '123@123.com', '123123123', 'admin', '0', '2017-06-02 08:53:43', '2017-06-02 08:53:43']
        values=["'%s'" %v[0] for k,v in register_info.items() if k!="repwd"]
        #如果name data password任一个为空，则报错
        if not username or not role or not password:
            errmsg='username,role and password can not be empty'
            return render_template("register.html",result=errmsg)
        # 如果2个密码输入的不一致，则报错
        if password != repwd:
            errmsg='password is not matched'
            return render_template("register.html", result=errmsg)
        try:
            sql = 'insert into users (%s) values (%s)' % (','.join(fields), ','.join(values))
            cur.execute(sql)
            connect.commit()
            #print (sql)
            #print (register_info)
            return redirect('/userinfo?name=%s'% username)
        except:
            errmsg='insert failed'
            #print (sql)
            #print (register_info)
            #print (traceback.print_exc())
            return render_template('/register.html',result=errmsg)
    else:
        return render_template('/register.html')

@app.route('/update',methods=['GET','POST'])
def update():
    if not session.get('name',None):
        return redirect('/login')
    if request.method=="POST":
        data=dict(request.form)
        print (data)
        #{'id': ['16'], 'name': ['1234'], 'email': ['123@123.com'], 'mobile': ['123123123'], 'role': ['admin'], 'status': ['0']}
        conditions=[ "%s='%s'" % (k,v[0]) for k,v in data.items() ]
        sql = 'update users set %s where id =%s' %(','.join(conditions),data['id'][0])
        print (sql)
        cur.execute(sql)
        return redirect ('/userlist')
    else:
        id = request.args.get('id',None)
        if not id:
            errmsg="must have id"
            return render_template('/update.html',result=errmsg)
        fields = ['id','name', 'email', 'mobile','role','status']
        try:
            sql='select %s from users where id=%s' %(','.join(fields),id)
            cur.execute(sql)
            result=cur.fetchone()
            user = dict((k, result[i]) for i, k in enumerate(fields))
            return render_template('/update.html',user=user)
        except:
            errmsg='get one failed'
            print (sql)
            return render_template('/update.html', result=errmsg)

@app.route('/changepwd',methods=['GET','POST'])
def changepwd():
    if not session.get('name',None):
        return redirect('/login')
    #将get参数id=21传递给POST
    #http://9.115.28.239:9092/changepwd?id = 21
    if request.method == "GET":
        id = request.args.get('id', None)
        return render_template('/changepwd.html',userid=id)
    if request.method == "POST":
        #获取表单数据
        data=dict(request.form)
        #表单数据转为字典{'id': '21', 'oldpwd': '123', 'newpwd': '123', 'repwd': '123'}
        passwd_info=dict((k, v[0]) for k, v in data.items())
        if not passwd_info['oldpwd'] or  not passwd_info['newpwd'] or  not passwd_info['repwd']:
            errmsg="can not be null"
            return render_template('/changepwd.html',result=errmsg)
        if passwd_info['newpwd']!=passwd_info['repwd'] :
            errmsg="password is not matched"
            return render_template('/changepwd.html',result=errmsg)
        sql="select password from users where id=%s" %(passwd_info['id'])
        cur.execute(sql)
        result=cur.fetchone()
        print (result)
        #('123',)
        if passwd_info['oldpwd']!= result[0]:
            errmsg = "old password is not correct"
            return render_template('/changepwd.html', result=errmsg)

        conditions = "password=%s" % passwd_info['newpwd']
        sql = 'update users set %s where id=%s' % (conditions, passwd_info['id'])
        cur.execute(sql)
        return redirect('/userlist')


@app.route('/delete')
def delete():
    if not session.get('name',None):
        return redirect('/login')
    id = request.args.get('id',None)
    try:
        sql='delete from users where id=%s' %id
        cur.execute(sql)
        return redirect('/userlist')
    except:
        errmsg='get one failed'
        print (sql)
        return render_template('/delete.html', result=errmsg)


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #一行代码 获得表单数据
        login_info_dict = dict(request.form)
        #print (login_info_dict)
        #login_info_dict结构{'name': ['123'], 'password': ['123']}
        #从字典取值，最好用get方法，如果name为空的话，默认赋值None 不会报错
        login_info=dict((k, v[0]) for k, v in login_info_dict.items())
        #print (login_info)
        #{'name': '123', 'password': '123'}
        username=login_info.get('name',None)
        password=login_info.get('password',None)
        if not username or not password :
            errmsg='name and password can not be empty'
            return render_template("login.html",result=errmsg)
        fields = ['name', 'password','role']
        sql="select %s from users where name=%s" %(','.join(fields),login_info['name'])
        cur.execute(sql)
        result = cur.fetchone()
        if not result:
            errmsg='this user  is not existed'
            return render_template('/login.html',result=errmsg)
        #user={}
        #将从数据库里面取的值，存入字典 ｛'name':'123','password':'123'｝
        user = dict((k, result[i]) for i, k in enumerate(fields))
        print ("user is: %s" %user)
        if user['password'] != password:
            errmsg='the password is not correct'
            return render_template('/login.html',result=errmsg)
        else:
            #登录成功 创建一个session 并且转入userinfo页面
            session['name']=login_info['name']
            session['role']=user['role']
            return redirect("/userinfo?name=%s" % username)
    else:
        return render_template('/login.html')

@app.route('/logout')
def logout():
    session.pop('name')
    session.pop('role')
    return redirect('/login')

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)