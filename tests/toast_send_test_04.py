# pip install win11toast

# 更复杂的Toast示例
# A more complex Toast example

from win11toast import toast
from pathlib import Path

image = {
    'src': Path(r'./images/hero.png').absolute().as_posix(),
    'placement': 'hero'
}

toast(
    'Hello',
    'Hello from Python',
    image=image,
    icon=Path(r'./images/icon.png').absolute().as_posix(),
    button={'activationType': 'protocol', 'arguments': 'https://google.com', 'content': 'Open Google'},
    app_id="MyToastTest"
)
