from command import *
import urllib2
class ConvoStarter(Command):
    def run(self,sender,msg,target):
        try:
            req=urllib2.Request('http://en.wikipedia.org/wiki/Special:Random')
            req.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
            res=urllib2.urlopen(req)
            self.cmdprocessor.sendmsg('What do you think of '+res.geturl()+' ?',target)
        except urllib2.HTTPError, e:
            self.cmdprocessor.sendmsg('The server couldn\'t fulfill the request.  Error code: '+e.code,target)
        except urllib2.URLError, e:
            self.cmdprocessor.sendmsg('Failed to reach a server:  '+e.reason,target)
    def getname(self):
        return "convo"
    def printhelp(self):
        return #TODO