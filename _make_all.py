# -*- coding: utf-8 -*-
import os
os.makedirs("frontend-pc/src/views", exist_ok=True)
def CH(*c): return "".join(chr(x) for x in c)
def W(p,c):
    with open(p,"w",encoding="utf-8") as f:
        f.write(c)
print("ready")
