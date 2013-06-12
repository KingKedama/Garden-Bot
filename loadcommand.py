from command import *
import sqlite3

class LoadCommand(Command):

    admin=True
    def run(self,sender,msg,target):
        args=msg.split()
        if len(args) != 4:
            self.cmdprocessor.sendmsg('Syntax: !%s [filename] [classname] [commandname]' % (self.name),target)
            return
        if args[3].lower() in self.cmdprocessor.commands:
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
        
class RemoveCommand(Command):

    admin=True
    
    def run(self,sender,msg,target):
        args=msg.split()
        if len(args) != 2:
            self.cmdprocessor.sendmsg('Syntax: !%s [commandname]' % (self.name),target)
            return
        if args[1].lower() not in self.cmdprocessor.commands:
            self.cmdprocessor.sendmsg('%s is not a command' % args[1],target)
            return
        del self.cmdprocessor.commands[args[1].lower()]
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('DELETE FROM commands WHERE name=? COLLATE nocase',(args[1],))
        conn.commit()
        conn.close()
        self.cmdprocessor.sendmsg('removed %s successfully' % (args[1]),target)
        
class ReloadCommand(Command):
    admin=True
    def run(self,sender,msg,target):
        args=msg.split()
        if len(args) != 2:
            self.cmdprocessor.sendmsg('Syntax: !%s [commandname]' % (self.name),target)
            return
        if args[1].lower() not in self.cmdprocessor.commands:
            self.cmdprocessor.sendmsg('%s is not a command' % args[1],target)
            return
        conn= sqlite3.connect(self.database)
        c=conn.cursor()
        c.execute('SELECT * FROM commands WHERE name=? COLLATE nocase',(args[1],))
        command=c.fetchone()
        result=self.cmdprocessor.add_command(command[1],command[2],command[0])
        if not result:
            self.cmdprocessor.sendmsg('failed to find class %s in %s' % (command[2],command[1]),target)
            return
        if not isinstance(result,Command):
            self.cmdprocessor.sendmsg('%s is not a Command' %(args[2]),target)
            return
        self.cmdprocessor.sendmsg('reloaded %s successfully' % (args[1]),target)