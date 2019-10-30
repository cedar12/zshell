#coding:utf-8
import zshell,sys,os

app=zshell.App({'prefix':'shell:>','error':u'错误，未找到命令{0}','ignore_case':True})

@app.shell
def add(args):
    num=0
    for i in args:
        num=num+i
    return num

@app.shell
def echo(args):
    str_arg=''
    for i in args:
        str_arg+=i
    return str_arg
@app.shell
def none():
    pass
@app.shell
def order(a,b,c):
    print(a,b,c)
    pass
@app.shell(desc='含有以下参数',args=[{'name':'status','desc':'退出状态'}])
def exit(status=0):
    print('退出')
    sys.exit(0)

@app.shell
def rm(f=None,r=None,_=None):
    a=1
    print(f,r,_)
    print('rm')
    return 'fail rm'

@app.shell
def ls():
    list=os.listdir('./')
    for path in list:
        print path+'\t\t'+str(os.path.getsize(path))+'字节'

@app.shell
def cd(args):
    os.chdir(args[0])

@app.shell
def pwd(args):
    return os.getcwd()




if __name__ == '__main__':
    app.run()