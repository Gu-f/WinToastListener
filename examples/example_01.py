# 常规
# Base Usage
from wintoastlistener import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


listener = ToastListener(callback=example_callback)
listener.listen()
