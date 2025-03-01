from src.toast_listener.subscriber import ToastListener


def example_callback(event_data, resources):
    print(event_data)
    print(resources)


toast_listener = ToastListener(example_callback, app_id="MyToastTest")  # 获取Toast内容以及事件信息
# toast_listener = ToastListener(example_callback, app_id="MyToastTest", fetch_toast_content=False)  # 只获取事件信息

toast_listener.listen()
