import socket
import time
import CrawThread
import glovar
import urllib.request
import re
from html.parser import HTMLParser, HTMLParseError

linklist=[]  
linkparse=""   
class URLParser(HTMLParser):
    def __init__(self,strict=False):
        self.in_form = False
        self.in_href = False
        self.current_hreflink=" "
        self.current_actionlink=" "
        self.current_forminputlist=[]
        self.linklist = []
        HTMLParser.__init__(self,strict=False)
    def handle_startendtag(self, tag, attrs):
        tag=tag.lower()
        if tag == 'input':
            if self.in_form:
                self.inputlistappend(attrs)
         
    def handle_starttag(self, tag, attrs):
#        print (tag)
        tag=tag.lower()
        if tag == 'a':
            self.hreflistappend(attrs)                
        elif tag == 'form':
            if not self.in_form:
                self.in_form = True
#                print ('formbegin!!')            
                self.current_actionlink = self.actionlink_from_attrs(attrs)   
                if not self.current_actionlink:
                    self.current_actionlink="NoActionLink"
        elif tag == 'input':
#            print("input")
            if self.in_form:
                self.inputlistappend(attrs)           
    def handle_endtag(self, tag):
        tag=tag.lower()
        if tag == 'a':
            if self.in_href:
                self.in_href = False
        elif tag == 'form':           
            if self.in_form:
                self.formlistappend()
                self.in_form = False
#                print('formend...')   
            
    def qualifiedlink(self,link):
        if "#" not in link and "javascript" not in link and link and link!="/":
            if "http" not in link:
                if link[0]=="/":
                    link=glovar.keyofdomain+link
                else:
                    link=self.currentparselink()+"/"+link
            if glovar.keyofdomain in link:
                return link           
        return None
    def currentparselink(self):
        global linkparse
        index=str.rfind(linkparse,"/")
        index1=str.rfind(linkparse,"//")+1
        if index!=index1:
            link=linkparse[:index]    
            return link 
        else:
            return linkparse
    def hrefdatadict_from_attrs(self, attrs):
        paradict = {}
        for prop, val in attrs:
            prop=prop.lower()
            if val and prop == 'href':                  
                self.in_href = True 
                qualifiedlink=self.qualifiedlink(val)
                if qualifiedlink:
                    self.linklistappend(qualifiedlink)
                    if qualifiedlink.count('?') == 1:
                        fields = qualifiedlink.split('?')
                        self.current_hreflink=fields[0]
                        parameters = fields[1]
                        para_list = parameters.split('&')
                        for item in para_list:
                            fields = item.split('=')
                            try: 
                                paradict[fields[0]] = fields[1]
                            except IndexError:
                                paradict[fields[0]] = None
                    return paradict
        return None 
    def actionlink_from_attrs(self, attrs):
        post_link =""
        for prop, val in attrs:
            prop=prop.lower()
            if  prop == 'action' and self.in_form: 
                    if val:             
                        post_link= self.qualifiedlink(val)
                    if post_link:
                        self.linklistappend(post_link)
                        return post_link
        return None       
    def inputlistappend(self, attrs):
        inputdict = dict()
        for prop, val in attrs:   
            if val:       
                inputdict[prop] = val
        if inputdict:
            self.current_forminputlist.append(inputdict)
    def hreflistappend(self,attrs):
        hrefdict={}
        dict = self.hrefdatadict_from_attrs(attrs)
        if dict:
            hrefdict[self.current_hreflink]=dict         
            flag=1
            glovar.hreflock.acquire()
            for idict in glovar.hreflist:
                if set(list(hrefdict))==set(list(idict)):
                    idictvalue=idict[list(idict)[0]]
                    hrefdictvalue=hrefdict[list(hrefdict)[0]]
                    if set(list(idictvalue))==set(list(hrefdictvalue)):
                        flag=0
            if flag==1:
                glovar.hreflist.append(hrefdict) 
                CrawThread.writetohreffile(hrefdict)  
            glovar.hreflock.release()             
    def formlistappend(self):
        formdict={}
        formdict[self.current_actionlink]=self.current_forminputlist
#   
#        for item in self.current_forminputlist:
#            self.current_forminputlist.remove(item)
        formstr=self.transformtostr(formdict)
        flag=1
        glovar.formlock.acquire()
#'''
#        for idict in glovar.formlist:
#            if set(list(idict))==set(list(formdict)):#link same
#                idictlist=idict[list(idict)[0]]
#                formdictlist=formdict[list(formdict)[0]]
#                for inputdict in formdictlist:
#                    for inputdict2 in idictlist:
#                        if set(list(inputdict))==set(list(inputdict2)):
#                            continue
#                        else:
#                            flag=0 
#'''    
        for form in glovar.formlist:
            str=self.transformtostr(form)
            if str==formstr:
                flag=0            
        if flag==1:
            glovar.formlist.append(formdict)  
            CrawThread.writetoformfile(formdict)  
        glovar.formlock.release()
        self.current_forminputlist=[]            
    def transformtostr(self,formdict):
        str=list(formdict)[0]  
        inputlist=formdict[str]
        for inputdict in inputlist:
            for item in inputdict:
                str+=item+inputdict[item]
        return str
    #complete the link
    def linklistappend(self,qualifiedlink):
        glovar.linklock.acquire()
        if qualifiedlink not in glovar.linklist:
            self.linklist.append(qualifiedlink)
            glovar.linklist.append(qualifiedlink)
            CrawThread.writetocrawfile(qualifiedlink)
        glovar.linklock.release()
class testparser():    
       def main(self,link):
#            global linkparse
#            linkparse=link
            timeout = 20 
            self.sleep_download_time = 10
            socket.setdefaulttimeout(timeout)
            url_parser = URLParser(strict=False)
#            headers = {
#           'User-Agent':
#           'Opera/9.23'
#             }
#                try:
#                    r = urllib.request.Request(link)
#                except ValueError as e:
#                    print("ValueError!!!")
#                    print(e)
#                    print("link:"+link+"\n")
#                    return 
#                if r:
            try:
                time.sleep(self.sleep_download_time)
                u = urllib.request.urlopen(link)
                backurl=u.geturl()#prevent redirection
                global linkparse
                linkparse=backurl
                print("backurl:",backurl)
                glovar.parselock.acquire()
                if backurl in glovar.parsedlist:
                    return None
                glovar.parselock.release()
                the_html = u.read()
                charset = u.info().get_content_charset()
                u.close() 
            except urllib.error.URLError as e:
                print(time.strftime("%Y-%m-%d %H:%M:%S"))
                print("fail to access!!!")
                print("urllib.error.URLError")
                print(e)
                print("link:"+link+"\n")
                return None
            except socket.timeout as e:
                print("socket timout:",link) 
                print(e)
                return None
#                    print ("charset:".join(charset))             
            if not charset:
                try:
                    url_parser.feed(the_html.decode('gb2312'))
                    print ('gb2312')
                except UnicodeDecodeError:
                    try:
                        url_parser.feed(the_html.decode('utf-8'))                    
                        print ('utf-8')
                    except UnicodeDecodeError:
                        try:
                            url_parser.feed(the_html.decode('GB18030'))
                            print ('GB18030')
                            #www.sohu.com
                        except HTMLParseError as e:
                            print(" HTMLParseError!!!")
                            print(e)
                            print("link:"+link+"\n")
                            return None
                        except UnicodeDecodeError as e:
                            print("UnicodeDecodeError")
                            print(e)
                            print("link:"+link+"\n")
                            return None
                except HTMLParseError as e:
                    print(" HTMLParseError:")
                    print(e)
                    print("link:"+link+"\n")
                    return None
                       
            else:
#                       try:
                print ("charset:"+charset)
                url_parser.feed(the_html.decode(charset))
#                            url_parser.feed(the_html)
#                        except Exception as e:
#                            print('parse error occurred: %s\n' % e)
#                            return None
                        
            global linklist 
            linklist= url_parser.linklist
            print(time.strftime("%Y-%m-%d %H:%M:%S"))
            print("parse successfully!!!")
            print("link parsed:"+link+"\n")
            return True
'''
        def getdomain(self,link):
            index1=str.find(link,"//")
#            print(index1)
            index2=str.find(link,"/",index1+2)
            if index2==-1:
                domain=link
            else:
#                print(index2)
                domain=link[0:index2]
            return domain
'''  
