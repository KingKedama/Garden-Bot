import Queue,string,thread,sqlite3,os,imp

class CmdProcessor:

    def __init__(self, inqueue,outqueue,bot):
        
        self.inqueue=inqueue
        self.outqueue=outqueue
        self.database=bot.database
        self.nick=bot.nick
        self.channel=bot.channel
        
        thread.start_new(self.run,())
        
    
    
    def run(self):
        self.commands={}
        self.add_command('roll','DiceRoller')#TODO get commands to load from database
        self.add_command('snuggle','Snuggle')
        self.add_command('convoStarter','ConvoStarter')
        self.add_command('linecount','ShowLineCount')
        self.add_command('actioncount','ShowActionCount')
        self.priority=1
        while 1:
            mess=self.inqueue.get()
            msg = string.split(mess)
            if msg [1] == 'PRIVMSG' and msg[2] == self.nick:
                if msg[3][:2] == ":!"  and msg[3][2:].lower() in self.commands:
                    if self.commands[msg[3][2:].lower()].pm:
                        self.commands[msg[3][2:].lower()].run(msg[0],mess[mess.find(" :")+2:],getnick(msg[0]))
            elif msg [1] == 'PRIVMSG' and msg[2] == self.channel:
                self.countline(self.getnick(msg[0]),mess)
                if msg[3][:2] == ":!"  and msg[3][2:].lower() in self.commands:
                    if self.commands[msg[3][2:].lower()].channel:
                        self.commands[msg[3][2:].lower()].run(msg[0],mess[mess.find(" :")+2:],msg[2])
            self.inqueue.task_done()
            
            
            
    
    def sendmsg(self,msg,target):
        self.outqueue.put((self.priority,'PRIVMSG '+target+' :'+msg))
        self.priority+=1
    def sendaction(self,msg,target):
        self.outqueue.put((self.priority,'PRIVMSG '+target+' :\x01ACTION '+msg+'\x01'))
        self.priority+=1
        
    def getnick(self, hostnick):
        sendernickcolon = hostnick.split("!", 1)[0]
        return sendernickcolon.strip(':')
    def countline(self,nick,mess):
        column='messages'
        nick=nick.lower()
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
        
    def add_command(self,filename,classname):
        c=self.load_class_from_file(filename,classname,(self,self.database))
        if c:
            self.commands[c.getname()]=c
    def load_class_from_file(self,name,expected_class,args):
        class_inst = None
        py_mod=__import__(name)
        if hasattr(py_mod, expected_class):
            expected_class=getattr(py_mod,expected_class)
        class_inst =expected_class(*args) 
        return class_inst
    
