import Queue,string,thread,sqlite3,os,imp,re
from command import *

class CmdProcessor:

    def __init__(self, inqueue,outqueue,bot):
        
        self.inqueue=inqueue
        self.outqueue=outqueue
        self.database=bot.database
        self.nick=bot.nick
        self.channel=bot.channel
        print self.channel
        self.socket=bot.s
        self.priority=1
        self.whois={}
        self.lastnick=''
        self.thread=thread.start_new(self.run,())
        
    
    
    def run(self):
        self.commands={}
        self.load_from_database()  
        
        while 1:
            mess=self.inqueue.get()
            lines=mess.splitlines()
            if len(lines) ==1:
                msg = mess.split()
                if msg [1] == 'PRIVMSG' and msg[2] == self.nick:
                    if msg[3][:2] == ":!"  and msg[3][2:].lower() in self.commands:
                        if self.commands[msg[3][2:].lower()].pm and self.permission(self.commands[msg[3][2:].lower()],self.getnick(msg[0])):
                            self.commands[msg[3][2:].lower()].execute(msg[0],mess[mess.find(" :")+2:],self.getnick(msg[0]))
                elif msg [1] == 'PRIVMSG' and msg[2] in self.channel:
                    if msg[3][:2] == ":!"  and msg[3][2:].lower() in self.commands:
                        if self.commands[msg[3][2:].lower()].channel and self.permission(self.commands[msg[3][2:].lower()],self.getnick(msg[0])):
                            self.commands[msg[3][2:].lower()].execute(msg[0],mess[mess.find(" :")+2:],msg[2])
                    else:
                        self.countline(self.getnick(msg[0]),mess,msg[2])
                elif msg[1] == 'NICK':
                    oldnick= self.getnick(msg[0]).lower()
                    if oldnick in self.whois:
                        self.whois[msg[2][1:]]=self.whois[oldnick]
                        del self.whois[oldnick]
                elif msg[1] == 'JOIN':
                    self.handle_names(self.getnick(msg[0]),msg[2])
                elif msg[1] == 'PART':
                    oldnick= self.getnick(msg[0]).lower()
                    if oldnick in self.whois:
                        if msg[2] in self.whois[oldnick][2]:
                            self.whois[oldnick][2].remove(msg[2])
                        if not self.whois[oldnick][2]:
                            del self.whois[oldnick]
                elif msg[1] == 'QUIT':
                    oldnick= self.getnick(msg[0]).lower()
                    if oldnick in self.whois:
                        del self.whois[oldnick]
                    
            else:
                if ":End of /NAMES list." in lines[-1]:
                    for line in lines[:-1]:
                        self.handle_names(line[line.find(" :")+1:],lines[-1].split()[3])
                elif ":End of /WHOIS list." in lines[-1]:
                    for line in lines[:-1]:
                        msg=line.split()
                        if len(msg) > 1 and msg[1]=='330':
                            self.whois[msg[3].lower()][0]=msg[4].lower()
                            self.whois[msg[3].lower()][1]=1
            self.inqueue.task_done()
            
            
            
    
    def sendmsg(self,msg,target):
        self.outqueue.put((self.priority,'PRIVMSG '+target+' :'+msg))
        #self.countline(self.nick,msg,None) is borked
        self.priority+=1
    def sendaction(self,msg,target):
        self.outqueue.put((self.priority,'PRIVMSG '+target+' :\x01ACTION '+msg+'\x01'))
        #self.countline(self.nick,':\x01ACTION',None) is borked
        self.priority+=1
    def sendnotice(self,msg,target):
        self.outqueue.put((self.priority,'NOTICE '+target+' :'+msg))
        self.priority+=1
        
    def getnick(self, hostnick):
        sendernickcolon = hostnick.split("!", 1)[0]
        return sendernickcolon.strip(':')
    def countline(self,sender,mess,channel): #expects a str and not unicode
        
        nick=sender.lower()
       
        if nick.lower() in self.whois:
            nick=self.whois[nick][0]
        
        if ':\x01ACTION' in mess:
                messages=0
                actions=1
        else:
            messages=1
            actions=0
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('SELECT user_id FROM users WHERE nick=?',(nick,))
        result= c.fetchone()
        if result:
            id=result[0]
        else:
            c.execute('INSERT INTO users (nick,joined) VALUES(?,datetime("now"))',(nick,))
            conn.commit()
            c.execute('SELECT user_id FROM users WHERE nick=?',(nick,))
            id=c.fetchone()[0]
        
        c.execute('''INSERT OR REPLACE INTO user_data (user_id,channel,messages,actions,last_said,last_time) VALUES(?,?,
                             (SELECT SUM(messages) FROM user_data WHERE user_id=? and channel=?)+?,
                             (SELECT SUM(actions) FROM user_data WHERE user_id=? and channel=?)+?,
                            ?,
                            datetime("now"))''',(id,channel,id,channel,messages,id,channel,actions,('<'+sender+'>: '+mess[mess.find(" :")+2:].strip()).decode("utf-8",'replace')))
        conn.commit()
        conn.close()
        
    def add_command(self,filename,classname,name):
        c=self.load_class_from_file(filename,classname,(self,self.database))
        if c and isinstance(c,Command):
            c.name=name.lower()
            self.commands[name.lower()]=c
        return c
    def load_class_from_file(self,name,expected_class,args):
        class_inst = None
        try:
            mod_name,file_ext = os.path.splitext(os.path.split(name)[-1])
            if file_ext.lower() == '.py':
                py_mod = imp.load_source(mod_name, name)
            elif file_ext.lower() == '.pyc':
                py_mod = imp.load_compiled(mod_name, name)
            else:
                py_mod=__import__(name)
            if hasattr(py_mod, expected_class):
                expected_class=getattr(py_mod,expected_class)
                class_inst =expected_class(*args)
        except:
            pass
        return class_inst
    def load_from_database(self):
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        for row in c.execute('SELECT * FROM commands'):
            self.add_command(row[1],row[2],row[0])
        conn.close()
        
        
    def handle_names(self, names, channel):
        names=names.split()
        for name in names:
            flag,name=self.split_name_and_flag(name)
            if name.lower() in self.whois and not channel in self.whois[name.lower()][2]:
                self.whois[name.lower()][2].append(channel)   
            else:
                self.whois[name.lower()]=[name.lower(),0,[channel]]
                self.outqueue.put((self.priority,'WHOIS '+name))
    
    def split_name_and_flag(self,name):
        regex = re.compile('^([a-z])')
        if regex.search(name.lower()) or name[0] in "_\[]{}^`|":
            return "",name
        else:
            return name[0],name[1:]
    def permission(self,command,nick):
        if not command.admin:
            return True
        if not nick.lower() in self.whois or not self.whois[nick.lower()][1]:
            self.sendnotice('permission denied: you are not authenticated',nick)
            return False
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('SELECT is_admin FROM users WHERE nick=? collate nocase',(self.whois[nick.lower()][0],))
        result=c.fetchone()
        if result == None or not result[0]:
            self.sendnotice('permission denied',nick)
            conn.close()
            return False
        else:
            conn.close()
            return True
            