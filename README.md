![](https://img.shields.io/badge/zshell-1.1.3-blue) ![](https://img.shields.io/badge/license-MIT-000000.svg) ![](https://img.shields.io/badge/pypi-1.1.3-lightgrey)
----------------
# 介绍
使用zshell可快速构建命令行应用


# 安装
以下方式任选其一即可
> 方式一：pip安装
```shell
pip install -i https://pypi.org/project pyzshell
```
> 方式二：解压 dist/zshell-1.1.x.tar.gz 进入到zshell-1.1.x目录使用以下命令即可安装
```shell
python setup.py install
```

# 开始
## 编写第一个zshell应用
创建helloworld.py文件
导入模块
```python
import zshell

```
创建一个应用
```python
app=zshell.App()
```
编写命令
```python
@app.shell
def helloworld():
    return 'Hello World'
```
运行应用
```python
app.run()
```
完整代码
```python
#coding=utf-8
import zshell

app=zshell.App()

@app.shell
def helloworld():
    return 'Hello World'
    
if __name__ == '__main__':
    app.run()
```

运行helloworld.py文件

![图1](https://raw.githubusercontent.com/cedar12/zshell/master/example-images/helloworld-1.jpg)

### 交互式运行
python 文件.py
```shell
python helloworld.py
zshell:>>helloworld
Hello World
```
### 非交互式运行
python 文件.py 命令 参数
```shell
python helloworld.py helloworld
Hello World
```

## 参数
### 变长参数
新建add函数，函数参数为元组变长参数，参数名必须是args
```python
@app.shell
def add(*args):
    num=0
    for i in args:
        num+=i
    return num
```
输入``add 1 2 3``调用add命令,将参数值1，2，3相加得出结果为6
```shell
zshell:>>add 1 2 3
6
zshell:>>add 1 2 3 4
10
```
新建add2函数，函数参数为字典变长参数，参数名必须是kwargs
```python
@app.shell
def add2(**kwargs):
    return kwargs['a']+kwargs['b']
```
输入add2 -a 1 -b 1调用add2命令,相加得出结果为2

参数仅支持英文或以-、--开头的英文，-、--开头的参数zshell会自动去掉-、--符号
```shell
zshell:>>add2 -a 1 -b 1
2
zshell:>>add2 -a 1 -b 1 -c 1
2
```
### 非变长参数
新建add3函数，函数参数随意
```python
@app.shell
def add3(a=0,b=0,c=0):
    return a+b+c
```
输入add3 1 2 3调用add3命令,相加得出结果为6
```shell
zshell:>>add3 1 2 3
6
zshell:>>add3 1 2 3 4
6
zshell:>>add3 1
1
```

## `@app.shell`详解
将函数添加到zshell命令

| 参数 | 说明   | 类型  | 默认 |
|--	 |--	 |--   |--   |
| name | 命令名 使用\|可分隔多个命令名 | string  | 函数名 |
| desc | 命令描述 | string | ""    |
| args | 命令参数 | list | []    |




