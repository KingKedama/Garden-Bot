from command import *
import sqlite3

class ShowActionCount(Command):

    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) == 2:
            nick= parts[1].lower()
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT SUM(actions) FROM users WHERE nick=? COLLATE nocase',(nick,))
            result= c.fetchone()
            conn.close()
            if result != None:
                self.cmdprocessor.sendmsg('%s has done %s action(s) so far.' % (nick,result[0]),target)
            else:
                self.cmdprocessor.sendmsg('%s has done 0 action(s) so far.' % (nick),target)
        else:
            conn= sqlite3.connect(self.database)
            c=conn.cursor()
            c.execute('SELECT SUM(actions) FROM users WHERE nick=? COLLATE nocase',(self.cmdprocessor.getnick(sender).lower(),))
            result= c.fetchone()
            self.cmdprocessor.sendmsg('%s has done %s action(s) so far.' % (self.cmdprocessor.getnick(sender),result[0]),target)
            conn.close()

    def getname(self):
        return "actioncount"