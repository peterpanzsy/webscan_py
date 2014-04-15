import threading
import urlparser
import time
import glovar
import os
def getdomain(link):
    index1=str.find(link,"//")
    index2=str.find(link,"/",index1+2)
    if index2>0:
        glovar.keyofdomain=link[:index2]
    else:
        glovar.keyofdomain=link
def loadlinkdict():
    f=open("PHP.txt","r")
    link=f.readline()
    while link:
        if link[-1]=="\n":
            link=link[:-1] 
        if "http" not in link:
            if link[0]=="/":
                link=glovar.keyofdomain+link  
            else:
                link=glovar.keyofdomain+"/"+link
        glovar.linklock.acquire()
        if link not in glovar.linklist:
            loadlink(link)
#            glovar.linkqueue.put(link)
#            glovar.linklist.append(link)
#            writetocrawfile(link)
        glovar.linklock.release()
        link=f.readline()
def loadlink(link):
#    glovar.keyofdomain = "http://fist.xjtu.edu.cn"
#remove the last "/" from domain if exists
#    if glovar.keyofdomain[-1]=="/":
#        glovar.keyofdomain=glovar.keyofdomain[:-1] 
    glovar.linkqueue.put(link)
    glovar.linklist.append(link)   
    writetocrawfile(link)
def writetocrawfile(link):
    ftocraw=open("tocraw.txt","a")
    ftocraw.write(time.strftime("%Y-%m-%d %H:%M:%S")+" ")
    ftocraw.write(link+"\n")
    ftocraw.close()
def writetolinkfile(link):
    flink=open("links.txt","a")
    flink.write(time.strftime("%Y-%m-%d %H:%M:%S")+" ")
    flink.write(link+"\n")
    flink.close()
def writetohreffile(hrefdict):
    fhref=open("hreflist.txt","a")
    fhref.write(time.strftime("%Y-%m-%d %H:%M:%S")+" ")
    for item in hrefdict:
        fhref.write("%s "%item)
        for i in hrefdict[item]:
            fhref.write("%s:"%i)
            fhref.write ("%s "%hrefdict[item][i])
    fhref.write("\n")
    fhref.close()
def writetoformfile(formdict):
    fform=open("formlist.txt","a")
    fform.write(time.strftime("%Y-%m-%d %H:%M:%S")+" ")
    for iterm in formdict:
        fform.write("%s\n"%iterm)
        for i in formdict[iterm]:
            fform.write("input: ")
            for j in i:
                fform.write("%s:"%j)
                fform.write("%s "%i[j])
            fform.write("\n")
        fform.write("\n")
    fform.close()
def clearfile():
    try:
        os.remove("links.txt")
    except:
        pass  
    try:
        os.remove("hreflist.txt")
    except:
        pass  
    try:
        os.remove("formlist.txt")
    except:
        pass 
    try: 
        os.remove("tocraw.txt")
    except:
        pass  
         
class CrawThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
            parser=urlparser.testparser()
            while True:
                item=None
                try:
                    
                    item=glovar.linkqueue.get(True,30)#when queue is empty,then some thread may put links in it
                 
                except Exception as e:
                    print("queue is empty")
                    break
                if parser.main(item):
                    if item!=urlparser.linkparse:
                        print(item,"redict to: ",urlparser.linkparse)
                    glovar.parselock.acquire()
                    glovar.parsedlist.append(urlparser.linkparse)
                    glovar.parselock.release()
                    writetolinkfile(urlparser.linkparse)#links.txt parsed right link
                    print(time.strftime("%Y-%m-%d %H:%M:%S"))
                    print("access successfully!!!")
                    print(urlparser.linkparse)
#                    glovar.quelock.acquire()
                    if urlparser.linklist:
                        for link in urlparser.linklist:
                            glovar.linkqueue.put(link)
#                    glovar.quelock.release()
            print(self.name+" over...")
#            glovar.countlock.acquire()
#            glovar.count+=1
#            if glovar.count==glovar.num:#last thread over
#                glovar.overflag=1
#            glovar.countlock.release()
class crawler:
    def __init__(self,firstlink):
        self.firstlink=firstlink
        self.threadPool = []
    def crawmain(self):      
        loadlink(self.firstlink)
        getdomain(self.firstlink)
        print(glovar.keyofdomain)
#        loadlinkdict()
        j = 0
        while j <glovar.num:
            crawth=CrawThread()
            self.threadPool.append(crawth)
            crawth.start()
            j += 1
        print("num of threads running is:")
        print(len(self.threadPool))    
#            for th in self.threadPool:
#                th.join(30)   
#            self.threadPool = []    
        
        
if __name__=="__main__":
    clearfile()
#    firstlink="http://202.117.54.203:8080/ProRes/"
    firstlink="http://fist.xjtu.edu.cn/"
#    firstlink="http://std.xjtu.edu.cn/" 
#    firstlink="http://www.sina.com.cn"
#    firstlink="http://www.sohu.com"
    acrawler=crawler(firstlink)
    glovar.num=100
    acrawler.crawmain()
    print("scan begin!!!")
                
                
                