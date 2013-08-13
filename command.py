import sys,traceback
class Command:

    channel=True
    pm=True
    admin=False
    def __init__(self,cmdprocessor,database):
        self.cmdprocessor=cmdprocessor
        self.database=database
    def execute(self,sender,msg,target):
        try:
            self.run(sender,msg,target)
        except Exception as e:
            self.cmdprocessor.sendmsg("unhandled exception %s" % (e.__class__.__name__),target)
            traceback.print_exception(*sys.exc_info())
    def run(self,sender,msg,target):
        print('this command not implimented')
    def printhelp(self):
        return