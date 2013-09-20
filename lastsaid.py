from command import *
import sqlite3

class LastSaid(Command):

    pm=False #for now, otherwise needs an optional argument for channel
    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) != 2:
            self.cmdprocessor.sendmsg("Syntax !%s [nick]" % (self.name,),target)
            return
        nick=parts[1].lower()
        if nick in self.cmdprocessor.whois:
                nick=self.cmdprocessor.whois[nick][0]
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('Select user_id FROM users WHERE nick=?',(nick,))
        result= c.fetchone()
        if not result:
            self.cmdprocessor.sendmsg('%s is not in the database.' % (nick),target)
            return
        c.execute('Select last_said,last_time FROM user_data WHERE user_id=? and channel=?',(result[0],target))
        result=c.fetchone()
        conn.close()
        if result != None:
            self.cmdprocessor.sendmsg('%s [%s]' % (result[0].strip(),result[1]),target)
        else:
            self.cmdprocessor.sendmsg('%s is not in the database' % (nick,),target)
            