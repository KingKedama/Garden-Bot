from command import *
import string,random
class DiceRoller(Command):
    def getname(self):
        return "roll"
    def printhelp(self):
        return #TODO
    def run(self,sender,msg,target):
        split=string.split(msg.lower())
        if len(split) < 2:
            self.cmdprocessor.sendmsg('invalid syntax.',target)
            return
        ret=""
        for dice in split[1:]:
            num = string.split(dice,"d")
            if len(num) != 2:
                self.cmdprocessor.sendmsg("invalid syntax.",target)
                return
            try:
                amount=int(num[0])
                size=int(num[1])
                if size < 1:
                    self.cmdprocessor.sendmsg("Die size must be possitive",target)
                    return
                ret+=dice+'['
                for x in range(0,amount):
                    ret+=str(random.randint(1,size))
                    if x != amount -1:
                        ret+=','
                ret+='] '
            except exceptions.ValueError:
                self.cmdprocessor.sendmsg("invalid syntax.",target)
                return 
        self.cmdprocessor.sendmsg(ret,target)