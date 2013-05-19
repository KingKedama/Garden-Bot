import socket,string

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
	
irc_conn()
login(NICK)
join(CHANNEL)

while 1:

    buffer = s.recv(1024)
    msg = string.split(buffer)
    if msg[0] == "PING": #check if server have sent ping command
        send_data("PONG %s" % msg[1]) #answer with pong as per RFC 1459
    if msg [1] == 'PRIVMSG' and msg[2] == NICK:
        filetxt = open('./test/msg.txt', 'a+') #open an arbitrary file to store the messages
        nick_name = msg[0][:string.find(msg[0],"!")] #if a private message is sent to you catch it
        message = ' '.join(msg[3:])
        filetxt.write(string.lstrip(nick_name, ':') + ' -> ' + string.lstrip(message, ':') + '\n') #write to the file
        filetxt.flush() #don't wait for next message, write it now!


		
		
		
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
