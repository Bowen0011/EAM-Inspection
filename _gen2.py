# -*- coding: utf-8 -*-
import base64,os
os.makedirs("frontend-pc/src/views",exist_ok=True)
text=""
data = base64.b64decode(text).decode("utf-8")
print(data[:50])
