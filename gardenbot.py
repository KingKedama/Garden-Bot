import socket,string,random,urllib2

SERVER='leguin.freenode.net' #The server we want to connect to 
PORT=6667 #The connection port which is usually 6667 
NICK='gardenbot' #The bot's nickname 
IDENT='520916' 
REALNAME='gardenbot' 
OWNER='Zeffydragon' #The bot owner's nick 
CHANNEL='#test198' #The default channel for the bot readbuffer='' #Here we store all the messages from server

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Create the socket 

#open a connection with the server
def irc_conn():
    s.connect((SERVER, PORT))

#simple function to send data through the socket
def send_data(command):
    s.send(command + '\n')
    
#join the channel
def join(channel):
    send_data("JOIN %s" % channel)
	
#send login data (customizable)
def login(nick, username='gardenbot', password = None, realname='gardenbot', hostname='testhostname', servername='whatevenisthis'):
    send_data("USER %s %s %s %s" % (username, hostname, servername, realname))
    send_data("NICK " + nick)
def sendmsg(msg,target):
    send_data('PRIVMSG '+target+' :'+msg)
def roll(sender,msg,target):
    split=string.split(msg.lower())
    if len(split) < 2:
        sendmsg('invalid syntax.',target)
        return
    ret=""
    for dice in split[1:]:
        num = string.split(dice,"d")
        if len(num) != 2:
            sendmsg("invalid syntax.",target)
            return
        try:
            amount=int(num[0])
            size=int(num[1])
            ret+=dice+'['
            for x in range(0,amount):
                ret+=str(random.randint(1,size))
                if x != amount -1:
                    ret+=','
            ret+='] '
        except exceptions.ValueError:
            sendmsg("invalid syntax.",target)
            return 
    sendmsg(ret,target)

def convostarter(sender,msg,target):
    try:
        req=urllib2.Request('http://en.wikipedia.org/wiki/Special:Random')
        req.add_header('User-Agent',"Mozilla/5.0 (X11; U; Linux i686) Gecko/20071127 Firefox/2.0.0.11")
        res=urllib2.urlopen(req)
        sendmsg('What do you think of '+res.geturl()+' ?',target)
    except urllib2.HTTPError, e:
        sendmsg('The server couldn\'t fulfill the request.  Error code: '+e.code,target)
    except urllib2.URLError, e:
        sendmsg('Failed to reach a server:  '+e.reason,target)
commands= {
    ":!roll": roll,
    ":!convo": convostarter
}
help= {
    "roll": "",
    "convo": "gives a link to a random wikipedia page"
}

def helpcommand(sender,msg,target):
    return
irc_conn()
login(NICK)
join(CHANNEL)

while 1:
    buffer = s.recv(1024)
    msg = string.split(buffer)
    if msg[0] == "PING": #check if server have sent ping command
        send_data("PONG %s" % msg[1]) #answer with pong as per RFC 1459
    if msg [1] == 'PRIVMSG' and msg[2] == NICK:
        if 'dkzxcvnveieruv' in msg[3]: #makes the bot shut down, usefull while debugging, may take it out
            exit(0)
    if msg [1] == 'PRIVMSG' and msg[2] == CHANNEL:
        if msg[3].lower() in commands:
            input = buffer[buffer.find(" :")+2:]
            commands[msg[3].lower()](msg[0],input,msg[2])
    else:
        print buffer
		
		

		
#Everything below this is leftover from Zeffy's splatcode. I'm too lazy to rewrite it, since Kedama probably knows more than I do about python.





"""
def parsemsg(msg): 
    complete=msg[1:].split(':',1) #Parse the message into useful data 
    info=complete[0].split(' ') 
    msgpart=complete[1] 
    sender=info[0].split('!') 
    if msgpart[0]=='`' and sender[0]==OWNER: #Treat all messages starting with '`' as command 
        cmd=msgpart[1:].split(' ')
        if cmd[0]=='op': 
            s.send('MODE '+info[2]+' +o '+cmd[1]+'n') 
        if cmd[0]=='deop': 
            s.send('MODE '+info[2]+' -o '+cmd[1]+'n') 
        if cmd[0]=='voice': 
            s.send('MODE '+info[2]+' +v '+cmd[1]+'n') 
        if cmd[0]=='devoice': 
            s.send('MODE '+info[2]+' -v '+cmd[1]+'n') 
        if cmd[0]=='sys': 
            syscmd(msgpart[1:],info[2])

    if msgpart[0]=='-' and sender[0]==OWNER : #Treat msgs with - as explicit command to send to server 
        cmd=msgpart[1:] 
        s.send(cmd+'n') 
        print 'cmd='+cmd

def syscmd(commandline,channel): 
    cmd=commandline.replace('sys ','') 
    cmd=cmd.rstrip() 
    os.system(cmd+' >temp.txt') 
    a=open('temp.txt') 
    ot=a.read() 
    ot.replace('n','|') 
    a.close() 
    s.send('PRIVMSG '+channel+' :'+ot+'n') 
    return 0
"""
