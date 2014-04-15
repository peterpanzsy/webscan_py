import queue
import threading
linklist=[]#alllinks to request
parsedlist=[]
hreflist=[]
formlist=[]
keyofdomain=" " 
linkqueue=queue.Queue()
parselock=threading.Lock()
quelock=threading.Lock()
linklock=threading.Lock()
hreflock=threading.Lock()
formlock=threading.Lock()
overflag=0