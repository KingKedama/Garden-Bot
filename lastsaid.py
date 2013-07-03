from command import *
import sqlite3

class LastSaid(Command):


    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) != 2:
            self.cmdprocessor.sendmsg("Syntax !%s [nick]" % (self.name,),target)
            return
        nick=parts[1].lower()
        if nick in self.cmdprocessor.whois:
                nick=self.cmdprocessor.whois[nick]
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('Select last_said,last_time FROM users WHERE nick=? COLLATE nocase',(nick,))
        result=c.fetchone()
        conn.close()
        if result != None:
            self.cmdprocessor.sendmsg('%s [%s]' % (result[0].strip(),result[1]),target)
        else:
            self.cmdprocessor.sendmsg('%s is not in the database' % (nick,),target)
            