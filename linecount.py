from command import *
import sqlite3

class ShowLineCount(Command):


    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) == 2:
            nick= parts[1]
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT messages FROM users WHERE nick=?',(nick,))
            result= c.fetchone()
            if result != None:
                self.cmdprocessor.sendmsg('%s has sent %s lines so far.' % (nick,result[0]),target)
            else:
                self.cmdprocessor.sendmsg('%s is not in the database. Did you type the name correctly? Case sensitive.' % (nick),target)
        else:
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT messages FROM users WHERE nick=?',(self.cmdprocessor.getnick(sender),))
            result= c.fetchone()
            self.cmdprocessor.sendmsg('%s has sent %s lines so far.' % (self.cmdprocessor.getnick(sender),result[0]),target)

    def getname(self):
        return "linecount"