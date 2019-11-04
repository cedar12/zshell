#/usr/bin/env python
#coding=utf-8
import zshell
app=zshell.App()

@app.shell(desc='将俩数相加',args=[('a',['-a','--a']),('b',['-b','--b'])])
def add(a,b=0):
    print(a,b)
    return a+b
@app.shell(desc='退出',name='c')
def exit(a=None,b=None,c=None):
    return (a,b,c)
@app.shell(desc='接收字典变长参数命令')
def test(**kwargs):
    return kwargs

@app.shell(desc='接收元组变长参数命令')
def test1(*args):
    return (args)

if __name__ == '__main__':
    app.run()