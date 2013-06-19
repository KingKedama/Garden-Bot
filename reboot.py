from command import *
import os,sys,subprocess,socket
class Reboot(Command):

    admin=True
    
    def run(self,sender,msg,target):
        self.cmdprocessor.outqueue.put((self.cmdprocessor.priority,"QUIT rebooting"))
        self.cmdprocessor.outqueue.join()
        self.cmdprocessor.socket.shutdown(socket.SHUT_RDWR)
        self.cmdprocessor.socket.close()
        os.system("python "+sys.argv[0]+' -d '+ self.database)
        sys.exit(0)