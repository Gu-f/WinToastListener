import base64
from typing import Callable, Union

import win32event
import win32evtlog

from .exception import ToastParserException, ToastEvtSubscribeActionError, ToastEvtSubscribeActionUnknown
from .fetch_toast_payload import FetchToastPayload
from .utils import parse_windows_event, parse_toast_raw_payload


class ToastListener(object):
    EVENT_LOG_CHANNEL = "Microsoft-Windows-PushNotification-Platform/Operational"

    def __init__(
            self, callback: Callable[[dict, dict], None],
            app_id: str = None,
            fetch_toast_content: bool = True,
            wpndatabase_path: str = None,
    ):
        """
        ToastListener Core
        :param callback: 监听回调函数
        """
        self._evt_flags = None
        self._evt_sub_handle = None
        self._roll_signal_handle = None

        self.app_id = app_id
        self.callback = callback
        self.fetch_toast_content = fetch_toast_content
        self.wpndatabase_path = wpndatabase_path

    def parse_windows_event(self, event_data: str):
        return parse_windows_event(event_data)

    def event_filter(self, data: dict) -> bool:
        app_id = data.get("AppUserModelId")
        if not app_id:
            return False

        if app_id == '*':
            return True
        elif app_id == self.app_id:
            return True
        else:
            return False

    def _callback(self, action, user_context, event_handle):
        """
        事件触发回调
        :param action: 回调动作
        :param user_context: 用户上下文
        :param event_handle: 事件句柄
        :return: None
        """
        wpndb: Union[FetchToastPayload | None]
        wpndb = None
        if self.fetch_toast_content:
            wpndb = FetchToastPayload(wpndatabase_path=self.wpndatabase_path)
        if action == win32evtlog.EvtSubscribeActionDeliver:
            event_data = win32evtlog.EvtRender(event_handle, win32evtlog.EvtRenderEventXml)
            try:
                event_json_data = self.parse_windows_event(event_data)
            except Exception as e:
                raise ToastParserException(f"Toast xml parser exception - [{e}]")
            filter_status = self.event_filter(event_json_data)
            if filter_status:
                resources = {}
                if self.fetch_toast_content:
                    toast_raw_content = self.get_toast_payload(event_json_data, wpndb)
                    json_payload = self.parse_toast_payload(toast_raw_content)
                    resources = self.extract_resource_file(json_payload)
                self.callback(event_json_data, resources)

        elif action == win32evtlog.EvtSubscribeActionError:
            raise ToastEvtSubscribeActionError(f"Subscribe Action Error - [{action}] - [{event_handle}]")
        else:
            raise ToastEvtSubscribeActionUnknown(f"Subscribe Action Unknown - [{action}] - [{event_handle}]")

    def listen(self, roll_cycle=500):
        user_context = None
        self._evt_flags = win32evtlog.EvtSubscribeToFutureEvents  # 订阅新日志
        self._evt_sub_handle = win32evtlog.EvtSubscribe(self.EVENT_LOG_CHANNEL, self._evt_flags, None, self._callback, user_context)

        self._roll_signal_handle = win32event.CreateEvent(None, False, False, None)

        while True:
            status = win32event.WaitForSingleObject(self._roll_signal_handle, roll_cycle)
            if status == win32event.WAIT_OBJECT_0:
                break

    def unlisten(self):
        self._evt_sub_handle.Close()
        win32event.SetEvent(self._roll_signal_handle)

    def get_toast_payload(self, json_data: dict, wpndb) -> str:
        trace_id = json_data.get("TrackingId")
        if wpndb:
            return wpndb.get_payload(trace_id)
        return ""

    def parse_toast_payload(self, toast_row_payload: str) -> dict:
        result = parse_toast_raw_payload(toast_row_payload)
        return result

    def extract_resource_file(self, json_payload: dict) -> dict:
        images = json_payload.get("image", [])
        b64_images = []
        for img in images:
            with open(img.get("image_src"), "rb") as image_file:
                base64_img = base64.b64encode(image_file.read()).decode()
            b64_images.append({
                "image": base64_img,
                "placement": img.get("placement"),
            })
        return {
            "texts": json_payload.get("text", {}),
            "images": b64_images,
        }
