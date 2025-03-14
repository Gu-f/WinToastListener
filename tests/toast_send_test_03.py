# pip install win11toast

# 包含icon的Toast
# Toast with icon

from pathlib import Path
from win11toast import toast

# 在线icon
# Online icon
toast('Hello', 'Hello from Python', icon='https://images.dog.ceo/breeds/collie-border/n02106166_5607.jpg', app_id="MyToastTest")

# 本地icon
# Local icon
toast('Hello', 'Hello from Python', icon=Path(r'./images/icon.png').absolute().as_posix(), app_id="MyToastTest")
