from command import *
import sqlite3

class ShowLineCount(Command):


    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) == 2:
            nick= parts[1].lower()
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT SUM(messages) FROM users WHERE nick=? COLLATE nocase',(nick,))
            result= c.fetchone()
            conn.close()
            if result != None:
                self.cmdprocessor.sendmsg('%s has sent %s lines so far.' % (nick,result[0]),target)
            else:
                self.cmdprocessor.sendmsg('%s has sent 0 lines so far.' % (nick),target)
        else:
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT SUM(messages) FROM users WHERE nick=? COLLATE nocase',(self.cmdprocessor.getnick(sender).lower(),))
            result= c.fetchone()
            self.cmdprocessor.sendmsg('%s has sent %s lines so far.' % (self.cmdprocessor.getnick(sender),result[0]),target)
            conn.close()

    def getname(self):
        return "linecount"