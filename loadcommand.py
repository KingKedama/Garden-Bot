from command import *
import sqlite3

class LoadCommand(Command):

    admin=True
    def run(self,sender,msg,target):
        args=msg.split()
        if len(args) != 4:
            self.cmdprocessor.sendmsg('Syntax: !%s [filename] [classname] [commandname]' % (self.name),target)
            return
        if args[3] in self.cmdprocessor.commands:
            self.cmdprocessor.sendmsg('%s is already a command' % args[3],target)
            return
        result=self.cmdprocessor.add_command(args[1],args[2],args[3])
        if not result:
            self.cmdprocessor.sendmsg('failed to find class %s in %s' % (args[2],args[1]),target)
            return
        if not isinstance(result,Command):
            self.cmdprocessor.sendmsg('%s is not a Command' %(args[2]),target)
            return
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('INSERT INTO commands (name,filename,classname) VALUES(?,?,?)',(args[3],args[1],args[2]))
        conn.commit()
        conn.close()
        self.cmdprocessor.sendmsg('loaded %s successfully' % (args[3]),target)