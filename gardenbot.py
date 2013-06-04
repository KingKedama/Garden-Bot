import socket,string,sys,sqlite3,getopt,Queue
from cmdProcessor import * 
from sendProcessor import *

def main(argv):
    try:
        opts, args = getopt.getopt(argv,"hs:p:n:r:c:p:d:",["server=","port=","nick=","realname=","channel=","password=","database="])
    except getopt.GetoptError:
        sys.exit(1) #TODO print syntax
    kwargs={}
    for opt, arg in opts:
        if opt == '-h':
            sys.exit() #TODO print syntax
        elif opt in ("-s","--server"):
            kwargs['server']=arg
        elif opt in ("-p","--port"):
            kwargs['port']=int(arg)
        elif opt in ("-n","--nick"):
            kwargs['nick']=arg
        elif opt in ("-r","--realname"):
            kwargs['server']=arg
        elif opt in ("-c","--channel"):
            kwargs['channel']=arg
        elif opt in ("-p","--password"):
            kwargs['password']=arg
        elif opt in ("-d","--database"):
            kwargs['database']=arg
    bot= GardenBot(**kwargs)
    bot.start()
class GardenBot:

    def __init__(self,database='data.db',server=None,port=None,nick=None,realname=None,channel=None,password=None):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn= sqlite3.connect(database)
        self.database=database
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS settings(
                     key text,
                     value text,
                     PRIMARY KEY (key))''')
        c.execute('''CREATE TABLE IF NOT EXISTS users(
                     id INTEGER,
                     nick TEXT,
                     messages INTEGER DEFAULT 0,
                     actions INTEGER DEFAULT 0,
                     PRIMARY KEY (id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS commands(
                     name text,
                     filename text,
                     classname text,
                     PRIMARY KEY (name))''')
        conn.commit()
        c.execute('''INSERT OR IGNORE INTO commands (name,filename,classname) VALUES("load","loadcommand.py","LoadCommand")''')
        if server:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("server",?)''',(server,))
            self.server=server
        else:
            c.execute('SELECT value FROM settings WHERE key="server"')
            tmp= c.fetchone()
            if tmp:
                self.server=tmp[0]
            else:
                print 'No server specified'
                sys.exit(1)
        if port:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("port",?)''',(port,))
            self.server=server
        else:
            c.execute('SELECT value FROM settings WHERE key="port"')
            tmp= c.fetchone()
            if tmp:
                self.port=tmp[0]
            else:
                self.port=6667
        if nick:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("nick",?)''',(nick,))
            self.nick=nick
        else:
            c.execute('SELECT value FROM settings WHERE key="nick"')
            tmp= c.fetchone()
            if tmp:
                self.nick=tmp[0]
            else:
                print 'No nick specified'
                sys.exit(1)
        if realname:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("realname",?)''',(realname,))
            self.realname=realname
        else:
            c.execute('SELECT value FROM settings WHERE key="realname"')
            tmp= c.fetchone()
            if tmp:
                self.realname=tmp[0]
            else:
                self.realname='gardenbot'
        if channel:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("channel",?)''',(channel,))
            self.channel=channel
        else:
            c.execute('SELECT value FROM settings WHERE key="channel"')
            tmp= c.fetchone()
            if tmp:
                self.channel=tmp[0]
            else:
                print 'No channel specified'
                sys.exit(1)
        if password:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("password",?)''',(password,))
            self.password=password
        else:
            c.execute('SELECT value FROM settings WHERE key="password"')
            tmp= c.fetchone()
            if tmp:
                self.password=tmp[0]
            else:
                self.password=None
        conn.commit()
        conn.close()
        
    def start(self):
        self.outqueue=Queue.PriorityQueue()
        sender=SendProcessor(self.outqueue,self.s)
        self.irc_conn()
        self.login(self.nick,password=self.password,realname=self.realname)
        
        msgqueue=Queue.Queue()
        
        processor=CmdProcessor(msgqueue,self.outqueue,self)
        while 1:
            buffer = self.s.recv(1024)
            print buffer
            msg = string.split(buffer)
            if len(msg) >0:
                if msg[0] == "PING": #check if server have sent ping command
                    self.send_data("PONG %s" % msg[1],0) #answer with pong as per RFC 1459
                if msg[1]=="NOTICE" and 'Found your hostname' in buffer:
                    if self.password:
                        tmp = 'identify %s' % self.password
                        processor.sendmsg(tmp,'NickServ')
                    self.join(self.channel)
                else:
                    msgqueue.put(buffer)
            
    def irc_conn(self):
        self.s.connect((self.server, self.port))

    #simple function to send data through the socket
    def send_data(self,command,priority=1000):
        self.outqueue.put((priority,command + '\n'))
        
    #join the channel
    def join(self,channel):
        self.send_data("JOIN %s" % channel,2)
    
    #send login data (customizable)
    def login(self,nick, username='gardenbot', password = None, realname='gardenbot', hostname='testhostname', servername='whatevenisthis'):
        self.send_data("USER %s %s %s %s" % (username, hostname, servername, realname),0)
        self.send_data("NICK " + nick,1)
        

if __name__ == "__main__":
    main(sys.argv[1:])