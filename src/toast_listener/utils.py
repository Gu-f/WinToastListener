from xml.etree import ElementTree


def parse_windows_event(xml_string):
    namespace = {'ns': 'http://schemas.microsoft.com/win/2004/08/events/event'}
    root = ElementTree.fromstring(xml_string)

    def get_text(path):
        element = root.find(path, namespace)
        return element.text if element is not None else ""

    def get_attrib(path, attrib):
        element = root.find(path, namespace)
        return element.attrib.get(attrib, "") if element is not None else ""

    event_data = {
        'Provider Name': get_attrib(".//ns:Provider", "Name"),
        'Provider Guid': get_attrib(".//ns:Provider", "Guid"),
        'EventID': get_text(".//ns:EventID"),
        'Version': get_text(".//ns:Version"),
        'Level': get_text(".//ns:Level"),
        'Task': get_text(".//ns:Task"),
        'Opcode': get_text(".//ns:Opcode"),
        'Keywords': get_text(".//ns:Keywords"),
        'TimeCreated': get_attrib(".//ns:TimeCreated", "SystemTime"),
        'EventRecordID': get_text(".//ns:EventRecordID"),
        'ProcessID': get_attrib(".//ns:Execution", "ProcessID"),
        'ThreadID': get_attrib(".//ns:Execution", "ThreadID"),
        'Channel': get_text(".//ns:Channel"),
        'Computer': get_text(".//ns:Computer"),
        'UserID': get_attrib(".//ns:Security", "UserID"),
    }

    for data in root.findall(".//ns:EventData/ns:Data", namespace):
        name = data.attrib.get("Name", "Unknown")
        event_data[name] = data.text if data.text else ""

    return event_data


def parse_toast_raw_payload(xml_string):
    print(xml_string)
    root = ElementTree.fromstring(xml_string)

    visual = root.find('.//visual')

    texts = visual.findall('.//text')
    title = texts[0].text if len(texts) > 0 else ""
    detail_desc = texts[1].text if len(texts) > 1 else ""

    images = []
    for image in visual.findall('.//image'):
        image_data = {
            "image_name": image.get("src").split("\\")[-1],  # 提取图片的文件名
            "image_src": image.get("src"),
            "placement": image.get("placement")
        }
        images.append(image_data)

    result = {
        "text": {
            "title": title,
            "detail_desc": detail_desc
        },
        "image": images
    }

    return result
