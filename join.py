from command import *
import sqlite3

class JoinChannel(Command):

    admin=True
    def run(self,sender,msg,target):
        parts = msg.split()
        if len(parts) != 2:
            self.cmdprocessor.sendmsg("Syntax !%s [channel]" % (self.name,),target)
            return
        chan=parts[1]
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('''INSERT OR IGNORE INTO channels (channel) VALUES(?)''',(chan,))
        self.cmdprocessor.outqueue.put((2,"JOIN %s" % chan))