
# 介绍
使用zshell可快速构建命令行应用


# 安装
解压 zshell-1.0.0.tar.gz 进入zshell-1.0.0目录使用以下命令即可安装
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

![图1](https://github.com/cedar12/zshell/blob/master/example-images/helloworld-1.jpg)

