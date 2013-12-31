from command import *

class Echo(Command):

    admin=True
    def run(self,sender,msg,target):
        self.cmdprocessor.outqueue.put((self.cmdprocessor.priority,msg[msg.find(" ")+1:]))