import Queue,string,thread,sqlite3

class CmdProcessor:

    def __init__(self, inqueue,outqueue,bot):
        
        self.inqueue=inqueue
        self.outqueue=outqueue
        self.database=bot.database
        self.nick=bot.nick
        self.channel=bot.channel
        
        thread.start_new(self.run,())
        
    
    
    def run(self):
        #TODO set up command list
        while 1:
            mess=self.inqueue.get()
            msg = string.split(mess)
            if msg [1] == 'PRIVMSG' and msg[2] == self.nick:
                print 'pm'
            elif msg [1] == 'PRIVMSG' and msg[2] == self.channel:
                sendernickcolon = msg[0].split("!", 1)[0]
                sendernick = sendernickcolon.strip(':')
            self.inqueue.task_done()
            
            
            
    
    def sendmsg(self,msg,target,priority=1000):
        self.outqueue.put((priority,'PRIVMSG '+target+' :'+msg))
    def sendaction(self,msg,target,priority=1000):
        self.outqueue.put((priority,'PRIVMSG '+target+' :\x01ACTION '+msg+'\x01'))