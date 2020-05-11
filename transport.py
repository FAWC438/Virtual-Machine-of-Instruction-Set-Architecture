# 在
from register import *
from addressing import *

def rrMov(regA: Register, regB: Register):
    regA.readData()
    regB.writeData()

def irMov(imm, reg: Register):
    Register.BUS = imm
    reg.writeData()

def rmMov(reg: Register, AR: ARegister, DR: DRegister, memory: Memory):
    """

    :param reg:
    :param address:
    :return:
    """
    #地址已放到AR中
    reg.readData()
    DR.writeData()
    memory.writeData(AR, DR)

def mrMov(reg: Register, AR: ARegister, DR: DRegister, memory: Memory):
    #地址已放到AR中
    memory.readData(AR, DR)
    DR.readData()
    reg.writeData()

def cMov(regA: Register, regB: Register, psw: Psw, way):
    """
    条件传送
    :param regA:
    :param regB:
    :param psw:
    :param way: 'le': 0x1, 'l': 0x2,
                'e': 0x3, 'ne': 0x4,
                'ge': 0x5, 'g': 0x6
    :return:
    """
    if ((way == 0x1 and psw.lessEqual()) or
        (way == 0x2 and psw.less()) or
        (way == 0x3 and psw.equal()) or
        (way == 0x4 and not psw.equal()) or
        (way == 0x5 and psw.largeEqual()) or
        (way == 0x6 and psw.large())):
        rrMov(regA, regB)