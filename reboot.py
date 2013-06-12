from command import *
import os,sys
class Reboot(Command):

    admin=True
    
    def run(self,sender,msg,target):
        self.cmdprocessor.outqueue.put((0,"QUIT rebooting"))
        #subprocess.call(["python", "gardenbot.py", "-d", self.database])
        os.system("python "+sys.argv[0]+" gardenbot.py -d "+self.database)
        sys.exit(0)