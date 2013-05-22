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
                self.countline(self.getnick(msg[0]),mess)
            self.inqueue.task_done()
            
            
            
    
    def sendmsg(self,msg,target,priority=1000):
        self.outqueue.put((priority,'PRIVMSG '+target+' :'+msg))
    def sendaction(self,msg,target,priority=1000):
        self.outqueue.put((priority,'PRIVMSG '+target+' :\x01ACTION '+msg+'\x01'))
        
    def getnick(self, hostnick):
        sendernickcolon = hostnick.split("!", 1)[0]
        return sendernickcolon.strip(':')
    def countline(self,nick,mess):
        column='messages'
        if ':\x01ACTION' in mess:
                column='actions'
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('SELECT * FROM users WHERE nick=?',(nick,))
        result= c.fetchone()
        if result:
            c.execute('UPDATE users SET '+column +' = '+column+' + 1 WHERE nick=?',(nick,))
        else:
            c.execute('INSERT INTO users (nick,'+column+') VALUES(?,1)',(nick,))     
        conn.commit()
        conn.close()
        
        