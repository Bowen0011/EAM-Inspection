import os  
p=r"D:\DATA\¹¤¾ß\EAM-Inspection\frontend-pc\src\views"  
os.makedirs(p,exist_ok=True)  
def C(*c): return "".join(chr(x) for x in c)  
W=lambda n,c: open(p+"\\"+n,"w",encoding="utf-8").write(c)  
  
# UserManage.vue  
W("UserManage.vue","<template>\n<div>test</div>\n</template>")  
print("ok") 
