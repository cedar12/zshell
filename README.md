
# 介绍
使用zshell可快速构建命令行应用
![pip](https://img.shields.io/badge/zshell-1.1.0-blue)

# 安装
以下方式任选其一即可
> 方式一：pip安装
```shell
pip install -i https://pypi.org/project pyzshell
```
> 方式二：解压 dist/zshell-1.1.0.tar.gz 进入到zshell-1.1.0目录使用以下命令即可安装
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

## `@app.shell`详解
将函数添加到zshell命令

| 参数 | 说明   | 类型  | 默认 |
|--	 |--	 |--   |--   |
| name | 命令名 使用\|可分隔多个命令名 | string  | 函数名 |
| desc | 命令描述 | string | ""    |
| args | 命令参数 | list | []    |




