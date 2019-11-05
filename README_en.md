![](https://img.shields.io/badge/zshell-1.1.4-blue) ![](https://img.shields.io/badge/license-MIT-000000.svg) ![](https://img.shields.io/badge/pypi-1.1.4-lightgrey)
----------------

[中文](https://github.com/cedar12/zshell/blob/master/README.md) | [English](https://github.com/cedar12/zshell/blob/master/README_en.md)


# introduce
Use zshell to quickly build command-line applications


# install
Choose one of the following ways
> Option 1: PIP installation
```shell
pip install -i https://pypi.org/project pyzshell
```
> Mode 2: unzip dist/ zshell-1.1.x.tar.gz into zshell-1.1.x directory and install it using the following command
```shell
python setup.py install
```

# Quick start
## Write your first zshell application
Create the helloworld.py file
import module
```python
import zshell

```
Create an application
```python
app=zshell.App()
```
Write command
```python
@app.shell
def helloworld():
    return 'Hello World'
```
Run the application
```python
app.run()
```
The complete code
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

Run the helloworld.py file

![图1](https://raw.githubusercontent.com/cedar12/zshell/master/example-images/helloworld-1.jpg)

### Interactive operation
python file.py
```shell
python helloworld.py
zshell:>>helloworld
Hello World
```
### Non-interactive operation
python file.py command parameter
```shell
python helloworld.py helloworld
Hello World
```

## parameter
### Variable-length argument
Create a new add function with tuple variable-length arguments and args
```python
@app.shell
def add(*args):
    num=0
    for i in args:
        num+=i
    return num
```
Enter ``add 1, 2, 3`` to invoke the add command and add the parameter values 1, 2, 3 to get 6
```shell
zshell:>>add 1 2 3
6
zshell:>>add 1 2 3 4
10
```
Create a new add2 function that takes a dictionary-length argument with the name kwargs
```python
@app.shell
def add2(**kwargs):
    return kwargs['a']+kwargs['b']
```
Enter ``` add2-a 1-b 1 ``` to call the add2 command and add up to 2

The arguments only support English or English with -, --, and the arguments zshell automatically removes -, -- symbols
```shell
zshell:>>add2 -a 1 -b 1
2
zshell:>>add2 -a 1 -b 1 -c 1
2
```
### Nonvariable-length parameter
New add3 function, function parameters arbitrary
```python
@app.shell
def add3(a=0,b=0,c=0):
    return a+b+c
```
Enter ```add3 1 2 3``` to call the add3 command, and add up to 6
```shell
zshell:>>add3 1 2 3
6
zshell:>>add3 1 2 3 4
6
zshell:>>add3 1
1
```

## `@app.shell` Details to explain
Add the function to the zshell command

| parameter | instructions   | type  | default |
|--	 |--	 |--   |--   |
| name | Use \| to separate multiple command names | string  | The function name |
| desc | Command description | string | ""    |
| args | The command parameter | list | []    |


## version
* 1.1.4 
    * New built-in command clear
        * Clearance console
    * Fix known bugs


