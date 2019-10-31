import re,sys,subprocess,platform

class App():
    def __init__(self,prefix='zshell:>>',ignore_case=True,not_found_error='Command not found',args_not_match_error='The number of arguments does not match'):
        self.options={}
        self.options['prefix']=prefix
        self.options['ignore_case']=ignore_case
        self.options['not_found_error']=not_found_error
        self.options['args_not_match_error']=args_not_match_error
        self.cmd_list=[]
        self.cmd_help={}
        self.get_system_info()

    def get_system_info(self):
        sysstr = platform.system()
        self.system_name=sysstr

    def change_prefix(self,prefix):
        self.options['prefix']=prefix

    def handle_args(self):
        cmd_input = raw_input(self.options['prefix'])
        args=re.split(r'\s+', str(cmd_input).strip())
        for i in range(1,len(args)):
            try:
                args[i]=int(args[i])
            except:
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
                    args_list = []
                    for var in varnames:
                        for i in range(1, len(args) - 1, 2):
                            if (args[i].strip() == '-' + var or args[i].strip() == '--' + var) and var != '_':
                                args_list.append('{0}=\'{1}\''.format(var, args[i + 1]))
                        if var == '_':
                            for i in range(1, len(args)):
                                if args[i].startswith('-') or args[i].startswith('--'):
                                    continue
                                elif args[i - 1].startswith('-') or args[i - 1].startswith('--'):
                                    continue
                                elif i == 1 or not args[i - 1].startswith('-'):
                                    args_list.append('{0}=\'{1}\''.format(var, args[i]))
                                else:
                                    args_list.append('{0}={1}'.format(var, None))

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


