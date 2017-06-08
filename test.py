from flask import Flask, request, render_template
app=Flask(__name__)

@app.route('/bing')
def bingpage():
    users=[]
    f=open("user.txt")
    #列表生成试
    users = [line.rstrip('\n').split(':') for line in f]
    f.close()
    return render_template('test.html',users=users)

if __name__=='__main__':
    app.run(host='0.0.0.0',port=9092,debug=True)