import _thread,sys,time

class SendProcessor:

    def __init__(self,outqueue,socket,verbose):
        
        self.outqueue=outqueue
        self.s=socket
        self.verbose=verbose
        self.thread=_thread.start_new(self.run,())
        
    
    
    def run(self):
        count =1
        while 1:
            data=self.outqueue.get()[1]
            count+=1
            if self.verbose:
                print( 'sending: '+data)
            self.send_data(data)
            self.outqueue.task_done()
            if data=="QUIT rebooting":
                sys.exit(0)
            
            time.sleep(1)
            
    def send_data(self,data):
        if type(data) is str:
            data= data.encode('utf-8','replace')
        self.s.send(data + b'\n')