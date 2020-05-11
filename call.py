from register import PC, Register, ARegister, DRegister
from memory import Memory
from addressing import addRegIndir

def call(RSP: Register, AR: ARegister, DR: DRegister, memory: Memory, PC: PC, Reg: Register):
    """
    函数调用指令, 注意: 由于在寻址之前需要进行若干操作, 在函数内调用寻址函数
    :param RSP:
    :param AR:
    :param DR:
    :param memory:
    :param PC:
    :param Reg:
    :return:
    """
    RSP.data = RSP.data - 1

    RSP.readData()
    AR.writeData()

    PC.readData()
    DR.writeData()

    memory.writeData(AR, DR)
    
    Reg.readData()
    PC.writeData()


def ret(RSP: Register, AR: ARegister, DR: DRegister, memory: Memory, PC: PC):
    """
    函数返回指令
    :param RSP:
    :param AR:
    :param DR:
    :param memory:
    :param PC:
    :return:
    """
    RSP.readData()
    AR.writeData()

    memory.readData(AR, DR)

    DR.readData()
    PC.writeData()
    
    RSP.data = RSP.data + 1
    