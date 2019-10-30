import re,sys,subprocess,platform

class App():
    def __init__(self,options=None):
        self.handle_options(options)
        self.cmd_list=[]
        self.cmd_help={}

    def get_system_info(self):
        sysstr = platform.system()
        if (sysstr == "Windows"):
            print ("Call Windows tasks")
        elif (sysstr == "Linux"):
            print ("Call Linux tasks")
        else:
            print ("Other System tasks")

    def handle_options(self,options):
        if options==None:
            options={}
        try:
            options['error']
        except:
            options['error']='Command not found'
        try:
            options['error1']
        except:
            options['error1'] = 'The number of arguments does not match'
        try:
            options['prefix']
        except:
            options['prefix'] = '>>'
        try:
            options['ignore_case']
        except:
            options['ignore_case'] = True
        self.options=options

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

    def cmd(self,cmd,args=[],is_system=False):
        if len(args)>0:
            args.insert(0, cmd)
        else:
            args.append(cmd)
        if is_system:
            p=subprocess.Popen(args=' '.join(args),stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            p.wait()
            print(p.stdout.read())
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
                            print(help_str)
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
                            val = args[i]
                            var = varnames[i - 1]
                            try:
                                val = type(args[i])
                                args_list.append('{0}={1}'.format(var, args[i]))
                            except:
                                args_list.append('{0}=\'{1}\''.format(var, args[i]))
                        args_str = ','.join(args_list)
                        msg = eval('handle({0})'.format(args_str))
                        pass
                    else:
                        print(self.options['error1'])
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
                    print(msg)
                break
        if not isRun:
            print(self.options['error'].format(args[0]))

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


