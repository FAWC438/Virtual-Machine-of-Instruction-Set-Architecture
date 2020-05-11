from register import Register, ARegister, DRegister
from memory import Memory

def push(regA: Register, RSP: Register, AR: ARegister, DR: DRegister, memory: Memory):
    """
    将指定寄存器的值压入栈中
    :param regA:
    :param RSP:
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    RSP.data = RSP.data - 1

    RSP.readData()
    AR.writeData()

    regA.readData()
    DR.writeData()
    
    memory.writeData(AR, DR)


def pop(regA: Register, RSP: Register, AR: ARegister, DR: DRegister, memory: Memory):
    """
    将栈顶值弹出到指定寄存器
    :param regA:
    :param RSP:
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    RSP.readData()
    AR.writeData()

    memory.readData(AR, DR)

    DR.readData()
    regA.writeData()

    RSP.data = RSP.data + 1
