# 仅捕获Toast消息事件，不需要内容信息
# Only Toast message events are captured, no content information is required
from wintoastlistener import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


listener = ToastListener(callback=example_callback, fetch_toast_content=False)
listener.listen()
