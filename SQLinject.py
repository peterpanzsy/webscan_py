'''
Created on 2012-8-15

@author: zsy
'''
import glovar
#from .. myCrawler import CrawThread                                                                                         
#import myCrawler.glovar
#from SQLInjectionDet.hrefSQLdetect import *
#from SQLInjectionDet.formSQLdetect import *
from CrawThread import *
from hrefSQLdetect import *
from formSQLdetect import *
def scansite():
    firstlink=input("site: ")
    glovar.num=input("num of threads: ")
    glovar.num=int(glovar.num)
    crawlerth=crawler(firstlink)
    crawlerth.crawmain()
    print("begin scanning! ")
def gethrefdict():
    link=input("link: ")
    hrefdict={}
    paradict={}
    if link.count('?') == 1:
        fields = link.split('?')
        hreflink=fields[0]
        parameters = fields[1]
        para_list = parameters.split('&')
        for item in para_list:
            fields = item.split('=')
            try: 
                paradict[fields[0]] = fields[1]
            except IndexError:
                paradict[fields[0]] = None
        hrefdict[hreflink]=paradict
        return hrefdict
    else:
        return None
if __name__=="__main__":
    ch=input("S:scan whole site; G:Detect a get link; P:Detect a post form")
    if ch=="S":
        scansite()
        while glovar.overflag==0:
            continue
        if glovar.overflag==1:#scan over
            ch1=input("G:Detect hreflist; P:Detect formlist")
            if ch1=="G":
                print("begin test hreflist")
                for hrefdict in glovar.hreflist:#only single thread otherwise console can not deal the output
                    hrefsqldetect(hrefdict).hrefInject()
            if ch1=="P":
                print("begin test formlist")
                for formdict in glovar.formlist:
                    formsqldetect(formdict).formInject()
    if ch=="G":
        hrefdict=gethrefdict()
        if hrefdict:
            hrefsqldetect(hrefdict).hrefInject()
        else:
            print("incorrect link !") 
#form aside
            