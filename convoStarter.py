from command import *
import urllib.request, urllib.error, urllib.parse
class ConvoStarter(Command):
    def run(self,sender,msg,target):
        try:
            req=urllib.request.Request('http://en.wikipedia.org/wiki/Special:Random')
            req.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
            res=urllib.request.urlopen(req)
            self.cmdprocessor.sendmsg('What do you think of '+res.geturl()+' ?',target)
        except urllib.error.HTTPError as e:
            self.cmdprocessor.sendmsg('The server couldn\'t fulfill the request.  Error code: '+e.code,target)
        except urllib.error.URLError as e:
            self.cmdprocessor.sendmsg('Failed to reach a server:  '+e.reason,target)
            
    def printhelp(self):
        return #TODO