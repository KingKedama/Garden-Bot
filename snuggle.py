from command import *

class Snuggle(Command):


    def run(self,sender,msg,target):
        if len(msg.split()) == 2: #There is a better way to do this, I know it. But it works for now.
            self.cmdprocessor.sendaction('snuggles %s lovingly.' % msg.split()[1],target)
        else:
            self.cmdprocessor.sendaction('snuggles %s lovingly.' % self.cmdprocessor.getnick(sender),target)
       
    def getname(self):
        return "snuggle"