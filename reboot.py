from command import *
import os,sys,subprocess
class Reboot(Command):

    admin=True
    
    def run(self,sender,msg,target):
        self.cmdprocessor.outqueue.put((0,"QUIT rebooting"))
        os.system("python "+sys.argv[0]+' -d '+ self.database)
        sys.exit(0)