from command import *
import sqlite3

class ShowLineCount(Command):


    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) == 2:
            sender= parts[1]
        else:
            sender=self.cmdprocessor.getnick(sender)
        nick=sender.lower()
        if nick in self.cmdprocessor.whois:
            nick=self.cmdprocessor.whois[nick][0]
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('Select user_id FROM users WHERE nick=?',(nick,))
        result= c.fetchone()
        if not result:
            self.cmdprocessor.sendmsg('%s is not in the database.' % (sender),target)
            return
        c.execute('SELECT SUM(messages), SUM(actions) FROM user_data WHERE user_id=? and channel=? COLLATE nocase',(result[0],target))
        result= c.fetchone()
        conn.close()
        if result != None:
            self.cmdprocessor.sendmsg('%s has sent %s lines and %s actions so far.' % (sender,result[0],result[1]),target)
        else:
            self.cmdprocessor.sendmsg('%s has sent 0 lines so far.' % (sender),target)