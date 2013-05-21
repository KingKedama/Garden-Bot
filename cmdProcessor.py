import Queue,string,thread

class CmdProcessor:

    def __init__(self, inqueue,outqueue,bot):
        
        self.inqueue=inqueue
        self.outqueue=outqueue
        self.bot=bot
        thread.start_new(self.run,())
        
    
    
    def run(self):
        #TODO set up command list
        while 1:
            mess=self.inqueue.get()
            msg = string.split(mess)
            if msg [1] == 'PRIVMSG' and msg[2] == self.bot.nick:
                self.sendmsg('recieved pm',self.bot.channel)
            elif msg [1] == 'PRIVMSG' and msg[2] == self.bot.channel:
               
                self.sendmsg('hardcoded','#test198')
                self.sendmsg('saw message in channel',self.bot.channel)
            self.inqueue.task_done()
            
            
            
    
    def sendmsg(self,msg,target):
        self.outqueue.put('PRIVMSG '+target+' :'+msg)
    def sendaction(self,msg,target):
        self.outqueue.put('PRIVMSG '+target+' :\x01ACTION '+msg+'\x01')