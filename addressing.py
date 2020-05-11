from memory import Memory
from register import *
import ALU

# def addImm(imm):
#     """
#     立即寻址
#     :return: 立即数
#     """
#     return imm


def addDir(AR: ARegister, DR: DRegister, memory: Memory, address):
    """
    直接寻址，无需提前把数据放到BUS！！！
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    Register.BUS = address
    AR.writeData()
    # AR.readFromMeomory(memory)
    # DR.writeFromMemory(memory)

def addIndir(AR: ARegister, DR: DRegister, memory: Memory, address):
    """
    间接寻址
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    addDir(AR, DR, memory, address)
    memory.readData(AR, DR)
    DR.readData()
    AR.writeData()

# def addReg(Reg: Register):
#     """
#     寄存器寻址
#     :param Reg: 任意寄存器
#     :return: 将寄存器的数据放到总线上
#     """
#     Reg.readData()

def addRegIndir(Reg: Register, AR: ARegister, DR: DRegister, memory: Memory):
    """
    寄存器间接寻址
    :param Reg: 任意寄存器
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    addDir(AR, DR, memory, Reg.data)

def addIndex(indexReg: Register, base,
             AR: ARegister, DR: DRegister,
             memory: Memory,
             xReg: Register, yReg: Register, psw: Psw):
    """
    变址寻址，从IR中获得基址和变址寄存器，经运算后地址在AR
    :param indexReg: 变址寄存器
    :param base: 从IR中获得的基准地址
    :param AR:
    :param DR:
    :param memory:
    :param xReg: ALU的X寄存器
    :param yReg: ALU的Y寄存器
    :param psw: 状态寄存器
    :return:
    """
    Register.BUS = base
    xReg.writeData()
    indexReg.readData()
    yReg.writeData()
    ALU.add(xReg, yReg, psw)
    # addRegIndir(yReg, AR, DR, memory)
    yReg.readData()
    AR.writeData()


def addRelate(PC: PC, bias,
              AR: ARegister, DR: DRegister,
              memory: Memory,
              xReg: Register, yReg: Register, psw: Psw):
    """
    相对寻址，获得地址为(PC+bias)，运算后地址在AR
    :param PC: 程序计数器
    :param bias: 偏移量
    :param AR:
    :param DR:
    :param memory:
    :param xReg:
    :param yReg:
    :param psw:
    :return:
    """
    PC.readData()
    xReg.writeData()
    Register.BUS = bias
    yReg.writeData()
    ALU.add(xReg, yReg, psw)
    # addRegIndir(yReg, AR, DR, memory)
    yReg.readData()
    AR.writeData()

def addBase(baseReg: Register, bias,
            AR: ARegister, DR: DRegister,
            memory: Memory,
            xReg: Register, yReg: Register, psw: Psw):
    """
    基址寻址，与变址寻址对偶，地址在AR
    :param baseReg: 基址寄存器
    :param bias: 偏移量
    :param AR:
    :param DR:
    :param memory:
    :param xReg:
    :param yReg:
    :param psw:
    :return:
    """
    baseReg.readData()
    xReg.writeData()
    Register.BUS = bias
    yReg.writeData()
    ALU.add(xReg, yReg, psw)
    # addRegIndir(yReg, AR, DR, memory)
    yReg.readData()
    AR.writeData()

def addStack(RSP: Register, AR: ARegister, DR: DRegister, memory: Memory):
    addDir(AR, DR, memory, RSP.data)
