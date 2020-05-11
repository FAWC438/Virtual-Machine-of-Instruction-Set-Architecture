import time
import os
import logging
from msvcrt import getch
from memory import Memory
from transport import *
from jump import *
from call import *
from stack import *
from ALU import *
from other import *
from register import Register, Psw, PC, ARegister, DRegister, IRegister

commandContent = {}
memory = Memory()
registers = [Register() for i in range(16)]
psw = Psw()
pc = PC()
xReg = Register()
yReg = Register()
state = State()
AR = ARegister()
IR = IRegister()
DR = DRegister()
