# WinToastListener
[README_EN](./README_EN.md)  
一个用于监听Windows Toast通知消息的python库

![Demo](https://github.com/Gu-f/WinToastListener/blob/main/images/example.gif)  

## 支持平台  
**支持**  
Windows10 及以上

**未测试**  
Windows8  
P.S.: 无该系统，无法测试。欢迎有相关系统的进行测试，并告知我结论。  

**不支持**  
Windows7 及以下

## 安装

`pip install wintoastlistener`

## 最小使用样例

```python
from wintoastlistener import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


listener = ToastListener(callback=example_callback)
listener.listen()
```

[更多示例](./examples)

## 文档
[文档](https://github.com/Gu-f/WinToastListener/wiki/%E6%96%87%E6%A1%A3(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87))  