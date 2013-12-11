from command import *

class Echo(Command):

    admin=true
    def run(self,sender,msg,target):
        self.cmdprocessor.outqueue.put((self.cmdprocessor.priority,msg[msg.find(" "):]))