from register import *
from addressing import *


def jmp(reg: Register, PC: PC, AR: ARegister, DR: DRegister, memory: Memory):
    """
    跳转指令，仅支持寄存器间接寻址，寻址后将PC的值更新
    :param reg: 存地址的寄存器
    :param PC: 程序计数器
    :param AR:
    :param DR:
    :param memory:
    :return:
    """
    reg.readData()
    PC.writeData()


def cjmp(reg: Register, PC: PC,
         AR: ARegister, DR: DRegister, memory: Memory,
         psw: Psw,
         way):
    """
    凡条件跳转均调用此，way用来传指令，对应lgh同学的条件编码
    'le': 0x1, 'l': 0x2,
    'e': 0x3, 'ne': 0x4,
    'ge': 0x5, 'g': 0x6
    :param reg: 存地址的寄存器
    :param PC:
    :param AR:
    :param DR:
    :param memory:
    :param psw: 状态寄存器
    :param way: 条件编码
    :return:
    """
    if ((way == 0x1 and psw.lessEqual()) or
        (way == 0x2 and psw.less()) or
        (way == 0x3 and psw.equal()) or
        (way == 0x4 and not psw.equal()) or
        (way == 0x5 and psw.largeEqual()) or
            (way == 0x6 and psw.large())):
        jmp(reg, PC, AR, DR, memory)
