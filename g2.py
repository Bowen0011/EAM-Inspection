import os  
p=r"D:\DATA\¹¤¾ß\EAM-Inspection\frontend-pc\src\views"  
os.makedirs(p,exist_ok=True)  
def C(*a): return "".join(chr(x) for x in a)  
def W(n,c):  
    with open(p+"\\"+n,"w",encoding="utf-8") as f:  
        f.write(c)  
W("test2.txt","ok")  
print("done") 
