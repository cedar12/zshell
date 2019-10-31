#coding=utf-8
from __future__ import print_function
import re,sys,subprocess,platform


class App():
    def __init__(self,prefix='zshell:>>',ignore_case=True,not_found_error='Command {0} not found',args_not_match_error='The number of arguments does not match',not_found_args_error='Args {0} not found',info_print=True):

        print_str = '''
                                                                                
               *******    *******    *          *******    *          *         
                    *     *          *          *          *          *         
                  *       *******    *******    *******    *          *         
                *               *    *     *    *          *          *         
               *******    *******    *     *    *******    *******    *******   
                                                                                
            '''
        if info_print:
            print(print_str)

        self.options={}
        self.options['prefix']=prefix
        self.options['ignore_case']=ignore_case
        self.options['not_found_error']=not_found_error
        self.options['args_not_match_error']=args_not_match_error
        self.options['not_found_args_error']=not_found_args_error
        self.cmd_list=[]
        self.cmd_help={}
        self.get_system_info()

    def get_system_info(self):
        sysstr = platform.system()
        self.system_name=sysstr

    def change_prefix(self,prefix):
        self.options['prefix']=prefix

    def handle_input(self,input):
        input_list=list(input)
        si = 0
        ei = 0
        for i in range(0,len(input_list)):
            t=input_list[i]
            if (t=='\'' or t=='"') and input_list[i-1]==' ':
                si=i
            if (t=='\'' or t=='"') and (i==len(input_list)-1 or input_list[i+1]==' '):
                ei=i
            if ei>si and si!=0:
                for j in range(si,ei):
                    if input_list[j]==' ':
                        input_list[j]='_&_'
                si=0
                ei=0
        input=''.join(input_list)
        return input

    def handle_args(self):
        try:
            cmd_input = raw_input(self.options['prefix'])
        except:
            cmd_input=input(self.options['prefix'])
        cmd_input=self.handle_input(cmd_input)
        args=re.split(r'\s+', str(cmd_input).strip())
        for i in range(1,len(args)):
            args[i]=args[i].replace('_&_',' ')
            try:
                args[i]=int(args[i])
            except:
                args[i]=str(args[i]).replace('"','').replace('\'','')
                pass
        return args;
    def start(self):
        args=sys.argv[1:]
        if len(args)>0:
            for i in range(1, len(args)):
                try:
                    args[i] = int(args[i])
                except:
                    pass
            self.handle_cmd(args)
            return False
        return True
    def println(self,msg):
        if self.system_name=='Windows':
            try:
                print(msg.decode('GB2312'))
            except:
                print(msg)
        else:
            print(msg)

    def cmd(self,cmd,args=[],is_system=False):
        if len(args)>0:
            args.insert(0, cmd)
        else:
            args.append(cmd)
        if is_system:
            p=subprocess.Popen(args=' '.join(args),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            self.println(p.stdout.read())
        else:
            self.handle_cmd(args)
    def check_args(self,varnames,arg_name):
        if arg_name in varnames:
            return True
        else:
            return False

    def handle_args_match(self,varnames,args):
        args_list=[]
        prefix_args=[]
        u_args=args[1:]
        for i in range(len(u_args)-1,-1,-1):
            arg=str(u_args[i])
            var_arg=None
            del_arg=None
            for var in varnames:
                if (arg.startswith('-{0}'.format(var)) or arg.startswith('--{0}'.format(var))) and (arg!='-{0}'.format(var) or arg!='--{0}'.format(var)):
                    arg_val=arg.replace('-{0}'.format(var),'').replace('--{0}'.format(var),'')
                    var_arg=('-{0}'.format(var),arg_val)
                    del_arg=arg
                    break
            if var_arg!=None:
                prefix_args.append(var_arg)
                u_args.remove(del_arg)
            elif i<len(u_args)-1 and arg.startswith('-') or arg.startswith('--'):
                prefix_args.append((arg,u_args[i+1]))
                u_args.remove(u_args[i+1])
                u_args.remove(u_args[i])
        for i in range(0,len(u_args)):
            arg=u_args[i]
            if  self.check_args(varnames,'_{0}'.format(i + 1)):
                try:
                    arg=int(arg)
                    args_list.append('{0}={1}'.format('_{0}'.format(i + 1), arg))
                except:
                    args_list.append('{0}=\'{1}\''.format('_{0}'.format(i + 1), arg))
                    pass
            else:
                return str(i + 1)
        for arg in prefix_args:
            if self.check_args(varnames, arg[0].replace('-','').replace('--','')):
                try:
                    val=int(arg[1])
                    args_list.append('{0}={1}'.format('{0}'.format(arg[0].replace('-','').replace('--','')), val))
                except:
                    args_list.append('{0}=\'{1}\''.format('{0}'.format(arg[0].replace('-', '').replace('--', '')), arg[1]))
            else:
                return arg[0]
        print(args_list)
        return args_list

    def handle_cmd(self,args):
        cmd = args[0]
        if self.options['ignore_case']:
            cmd = cmd.upper()
        isRun = False
        for handle in self.cmd_list:
            cmd_name = handle.__name__
            if self.options['ignore_case']:
                cmd_name = cmd_name.upper()
            if cmd_name == str(cmd).strip():
                varnames = []
                vars = handle.__code__.co_varnames
                vars_count = handle.__code__.co_argcount
                for i in range(0, vars_count):
                    varnames.append(vars[i])
                is_order = True
                is_help=False
                for i in range(1, len(args)):
                    if str(args[i])=='-help' or str(args[i])=='--help':
                        is_help=True
                        break
                    elif str(args[i]).startswith('-') or str(args[i]).startswith('--'):
                        is_order = False
                        break
                msg = None
                if is_help:
                    try:
                        map=self.cmd_help[handle.__name__]
                        if len(map[1])>0:
                            help_str=map[0]+'\n'
                            params=map[1]
                            for i in range(0,len(params)):
                                param=params[i]
                                help_str+='{0}\t{1}'.format(param['name'],param['desc'])
                                if i<len(params)-1:
                                    help_str+='\n'
                            self.println(help_str)
                    except:
                        pass
                elif len(varnames) == 0 and len(args)==1:
                    msg = handle()
                elif len(args)==1 and len(handle.__defaults__)==len(varnames):
                    msg = handle()
                elif len(varnames) == 1 and varnames[0] == 'args':
                    args.remove(args[0])
                    msg = handle(args)
                elif is_order:
                    args_list = []
                    if len(varnames) == len(args) - 1:
                        for i in range(1, len(args)):
                            var = varnames[i - 1]
                            if type(args[i])==int:
                                args_list.append('{0}={1}'.format(var, args[i]))
                            else:
                                args_list.append('{0}=\'{1}\''.format(var, args[i]))
                        args_str = ','.join(args_list)
                        msg = eval('handle({0})'.format(args_str))
                        pass
                    else:
                        self.println(self.options['args_not_match_error'])
                else:
                    args_list = self.handle_args_match(varnames,args)
                    if type(args_list)==str:
                        self.println(self.options['not_found_args_error'].format(args_list))
                    else:
                        args_str = ','.join(args_list)
                        msg = eval('handle({0})'.format(args_str))
                isRun = True
                if msg != None:
                    self.println(msg)
                break
        if not isRun:
            self.println(self.options['not_found_error'].format(args[0]))

    def shell(self,desc,args=[]):
        if type(desc)!=str:
            self.cmd_list.append(desc)
            self.cmd_help[desc.__name__] = ('', [])
        else:
            def fun(handle):
                self.cmd_list.append(handle)
                self.cmd_help[handle.__name__] = (desc,args)
            return fun

    def run(self):
        is_run=self.start()
        while is_run:
            args = self.handle_args()
            if len(args)==0 or (len(args)==1 and args[0].strip()==''):
                continue
            self.handle_cmd(args)
