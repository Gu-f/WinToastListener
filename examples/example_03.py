# 仅捕获指定的AppId通知
# Only the specified AppId notifications are captured
from wintoastlistener import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


listener = ToastListener(callback=example_callback, app_id="Chrome")
listener.listen()
