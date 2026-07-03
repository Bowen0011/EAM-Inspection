# -*- coding: utf-8 -*-
import os
print("Starting vue generation...")
p = r"D:\DATA\工具\EAM-Inspection\frontend-pc\src\views"
os.makedirs(p, exist_ok=True)
def C(*c):
    return "".join(chr(x) for x in c)
