import socket,string,sys,sqlite3,getopt,queue
from cmdProcessor import * 
from sendProcessor import *

def main(argv):
    print(argv)
    try:
        opts, args = getopt.getopt(argv,"b:hs:p:n:r:c:w:d:a:v",["bnc=","server=","port=","nick=","realname=","channel=","password=","database=","admin=","verbose"])
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
            kwargs['realname']=arg
        elif opt in ("-c","--channel"):
            kwargs['channel']=arg
        elif opt in ("-w","--password"):
            kwargs['password']=arg
        elif opt in ("-d","--database"):
            kwargs['database']=arg
        elif opt in ("-a","--admin"):
            kwargs['admin']=arg
        elif opt in ("-b","--bnc"):
            kwargs['bnc']=arg  #1 if a bnc is being used,0 or not given otherwise
        elif opt in ("-v","--verbose"):
            kwargs['verbose']=True
        
            
    bot= GardenBot(**kwargs)
    bot.start()
class GardenBot:

    def __init__(self,database='data.db',server=None,port=None,nick=None,realname=None,channel=None,password=None,admin=None,bnc=None,verbose=None):
        self.s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        conn= sqlite3.connect(database)
        self.database=database
        c=conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS settings(
                     key text,
                     value text,
                     PRIMARY KEY (key))''')
        c.execute('''CREATE TABLE IF NOT EXISTS users(
                     user_id INTEGER,
                     nick TEXT,
                     is_admin INTEGER DEFAULT 0 NOT NULL,
                     joined Text,
                     PRIMARY KEY (user_id))''')
        c.execute('''CREATE TABLE IF NOT EXISTS commands(
                     name text,
                     filename text,
                     classname text,
                     PRIMARY KEY (name))''')
        c.execute('''CREATE TABLE IF NOT EXISTS channels(
                     channel text,
                     PRIMARY KEY(channel)
                    )''')
        c.execute('''CREATE TABLE IF NOT EXISTS user_data(
                     user_id INTEGER,
                     channel text,
                     messages INTEGER DEFAULT 0 NOT NULL,
                     actions INTEGER DEFAULT 0 NOT NULL,
                     last_said Text,
                     last_time Text,
                     PRIMARY KEY(user_id,channel))  ''')
        conn.commit()
        c.execute('''CREATE UNIQUE INDEX IF NOT EXISTS remove_case ON users (nick COLLATE NOCASE)''')    
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
                print('No server specified')
                sys.exit(1)
        if port:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("port",?)''',(port,))
            self.port=int(port)
        else:
            c.execute('SELECT value FROM settings WHERE key="port"')
            tmp= c.fetchone()
            if tmp:
                self.port=int(tmp[0])
            else:
                self.port=6667
        if bnc:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("bnc",?)''',(bnc,))
            self.bnc=int(bnc)
        else:
            c.execute('SELECT value FROM settings WHERE key="bnc"')
            tmp= c.fetchone()
            if tmp:
                self.bnc=int(tmp[0])
            else:
                self.bnc=0
        if nick:
            c.execute('''INSERT OR REPLACE INTO settings (key,value) VALUES("nick",?)''',(nick,))
            self.nick=nick
        else:
            c.execute('SELECT value FROM settings WHERE key="nick"')
            tmp= c.fetchone()
            if tmp:
                self.nick=tmp[0]
            else:
                print('No nick specified')
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
        self.channel=list()
        if channel:    
            for chan in channel.split():
                c.execute('''INSERT OR IGNORE INTO channels (channel) VALUES(?)''',(chan,))
                self.channel.append(chan)
        c.execute('SELECT * FROM channels')
        tmp= c.fetchall()
        for chan in tmp:
            if not chan[0] in self.channel:
                self.channel.append(chan[0])
        if not self.channel:
            print('No channel specified')
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
        if admin:
            for name in admin.split():
                name=name.lower()
                c.execute('''SELECT * FROM users WHERE nick=?''',(name,))
                if c.fetchone():
                    c.execute('''UPDATE users SET is_admin=1 WHERE nick=?''',(name,))
                else:
                    c.execute('''INSERT INTO users (nick,is_admin) VALUES(?,1)''',(name,))
        conn.commit()
        conn.close()
        if verbose:
            self.verbose=True
        
    def start(self):
        self.outqueue=queue.PriorityQueue()
        sender=SendProcessor(self.outqueue,self.s,self.verbose)
        self.irc_conn()
        if self.bnc:
            self.login(self.nick,realname=self.realname)
            self.bnclogin(self.password)
        else:
            self.login(self.nick,password=self.password,realname=self.realname)
            
        self.badnumbers=['332','333']
        self.msgqueue=queue.Queue()
        
        self.processor=CmdProcessor(self.msgqueue,self.outqueue,self)
        save=""
        self.count=0
        while 1:
            try:
                buffer = self.s.recv(1024)
                buffer = buffer.decode('utf-8','replace')
            except Exception as e:
                print(e)
                sys.exit(0)
            self.line=0
            self.count+=1
            if len(buffer.splitlines()) ==1 and save =="": 
                self.process_input(buffer)
            else:
                if save != "":
                    buffer=save+buffer
                    save == ""
                lines=buffer.splitlines(True)
                for line in lines:
                    self.line+=1
                    msg=line.strip().split()
                    if len(msg) >1 and self.is_single_line(msg[1]):
                        self.process_input(line.strip())
                    else:
                        save+=line
                        if " :End of /" in line:
                            self.process_input(save)
                            save= ""
    
    def is_single_line(self,code):
        if not code.isdigit():
            return True
        if code in self.badnumbers:
            return True
        return False
    def process_input(self,buffer):
        if self.verbose:
            print( '%d:%d %s'  % (self.count,self.line,buffer))
        msg = buffer.split()
        if len(msg) >0:
            if msg[0] == "PING": #check if server have sent ping command
                self.send_data("PONG %s" % msg[1],0) #answer with pong as per RFC 1459
            if msg[1]=="NOTICE" and ('Found your hostname' in buffer or 'Couldn\'t look up your hostname' in buffer):
                if self.password:
                    tmp = 'identify %s' % self.password
                    self.processor.sendmsg(tmp,'NickServ')
                for chan in self.channel:
                    self.join(chan)
            else:
                self.msgqueue.put(buffer)
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
        
    def bnclogin(self,userpwd):
        self.send_data("PASS %s" % (userpwd),0)
        

if __name__ == "__main__":
    main(sys.argv[1:])
