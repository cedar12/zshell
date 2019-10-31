#coding:utf-8
import zshell,sys,os

'''
prefix:                     命令输入显示前缀            默认：zshell:>>
not_found_error:            不存在的命令提示信息        默认：Command not found
args_not_match_error：      命令参数错误提示信息        默认：The number of arguments does not match
ignore_case:                命令忽略大小写             默认：True

'''
app=zshell.App(not_found_error=u'错误，未找到命令{0}',args_not_match_error=u'参数错误')

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
def none(args):
    app.cmd(cmd='add',args=args)
    app.cmd(cmd='ping',args=['127.0.0.1'],is_system=True)
    return 'none 运行结束'
@app.shell
def order(a,b,c):
    print(a,b,c)
    pass
@app.shell(desc='退出程序命令\n\t含有以下参数',args=[{'name':'status','desc':'退出状态'},{'name':'测试','desc':'测试参数'}])
def exit(status=0):
    print('退出',status)
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
        print(path+'\t\t'+str(os.path.getsize(path))+'字节')

@app.shell
def cd(args):
    os.chdir(args[0])

@app.shell
def pwd(args):
    return os.getcwd()




if __name__ == '__main__':
    app.run()