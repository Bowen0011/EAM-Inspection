import base64,sys
d=sys.argv[1]
open("output.txt","wb").write(base64.b64decode(d))
