class Command:

    channel=True
    pm=True
    admin=False
    def __init__(self,cmdprocessor,database):
        self.cmdprocessor=cmdprocessor
        self.database=database
    def run(self,sender,msg,target):
        print 'this command not implimented'
    def printhelp(self):
        return