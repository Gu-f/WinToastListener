# pip install win11toast

# 包含url的Toast
# Toast with url

from win11toast import toast

toast('Hello Python', 'Click to open url', on_click='https://www.python.org', app_id="MyToastTest")
