from command import *
import sqlite3

class ExceptThis(Command):

    admin=True
    def run(self,sender,msg,target):
        target[10000]