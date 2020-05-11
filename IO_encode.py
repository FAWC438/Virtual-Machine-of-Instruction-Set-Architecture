import time
import os
import logging

# 初始化logging包
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
handler = logging.FileHandler("log.txt", encoding="utf-8", mode="w")
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s - %(message)s')
handler.setFormatter(formatter)

console = logging.StreamHandler()
console.setLevel(logging.INFO)

logger.addHandler(handler)
logger.addHandler(console)

#   15个通用寄存器
normalRegisters = {'rax': 0x0, 'rcx': 0x1,
                   'rdx': 0x2, 'rbx': 0x3,
                   'rsp': 0x4, 'rbp': 0x5,
                   'rsi': 0x6, 'rdi': 0x7,
                   'r8': 0x8, 'r9': 0x9,
                   'r10': 0xA, 'r11': 0xB,
                   'r12': 0xC, 'r13': 0xD,
                   'r14': 0xE}

#   判断条件，0代表jmp，而rrmov有独立方法
judgements = {'le': 0x1, 'l': 0x2,
              'e': 0x3, 'ne': 0x4,
              'ge': 0x5, 'g': 0x6,
              'mp': 0x0}

#   寻址方式依次为：立即寻址，直接寻址，
#                   间接寻址，寄存器寻址，
#                   寄存器间寻址，变址寻址，
#                   相对寻址，基址寻址，
#                   堆栈寻址
addressingModes = {'imm': 0x0, 'dir': 0x1,
                   'ind': 0x2, 'reg': 0x3,
                   'inr': 0x4, 'mod': 0x5,
                   'rel': 0x6, 'bas': 0x7,
                   'sta': 0x8}

#   操作指令
oprations = {'cmp': 0x0, 'add': 0x1,
             'sub': 0x2, 'imul': 0x3,
             'div': 0x4, 'xor': 0x5,
             'or': 0x6, 'and': 0x7,
             'sal': 0x8, 'shl': 0x9,
             'sar': 0xA, 'shr': 0xB,
             'inc': 0xC, 'dec': 0xD}

#   rmmov寻址


def addressing_rm(mode, data, reg):
    baseNum = 0x4000000000000000
    #   未特别指明的寻址方式格式均为：MOED(DATA)
    baseReg = 0
    imm = 0

    if mode == 0x0 or mode == 0x1 or mode == 0x2:
        #   立即寻址，直接寻址，间接寻址
        baseReg = 0xF
        imm = int(data[2:], 16)

    elif mode == 0x3 or mode == 0x4:
        #   寄存器寻址，寄存器间寻址
        baseReg = normalRegisters[data]

    elif mode == 0x5 or mode == 0x7:
        #   变址寻址的格式为：mod(%Reg,$Imm)，基址寻址格式为：bas(%Reg,$Imm)
        baseReg = normalRegisters[data.split(',')[0]]
        imm = int(data.split(',')[1][2:], 16)

    elif mode == 0x6:
        #   相对寻址
        baseReg = 0xF  # 基址寄存器为PC
        imm = int(data[2:], 16)

    elif mode == 0x8:
        #   堆栈寻址的格式为：sta()
        baseReg = 0x4

    return baseNum ^ (mode << 14 * 4) ^ (reg << 13 * 4) ^ (baseReg << 12 * 4) ^ imm

#   mrmov寻址


def addressing_mr(mode, data, reg):
    baseNum = 0x5000000000000000
    #   未特别指明的寻址方式格式均为：MOED(DATA)
    baseReg = 0
    imm = 0

    if mode == 0x0 or mode == 0x1 or mode == 0x2:
        #   立即寻址，直接寻址，间接寻址
        baseReg = 0xF
        imm = int(data[2:], 16)

    elif mode == 0x3 or mode == 0x4:
        #   寄存器寻址，寄存器间寻址
        baseReg = normalRegisters[data]

    elif mode == 0x5 or mode == 0x7:
        #   变址寻址的格式为：mod(%Reg,$Imm)，基址寻址格式为：bas(%Reg,$Imm)
        baseReg = normalRegisters[data.split(',')[0]]
        imm = int(data.split(',')[1][2:], 16)

    elif mode == 0x6:
        #   相对寻址
        baseReg = 0xF  # 相当于基址寄存器为PC，此处0xF仅作占位用
        imm = int(data[2:], 16)

    elif mode == 0x8:
        #   堆栈寻址的格式为：sta()
        baseReg = 0x4

    return baseNum ^ (mode << 14 * 4) ^ (reg << 12 * 4) ^ (baseReg << 13 * 4) ^ imm


def encodeCommand(commandLine):
    command = commandLine.split()
    head = command[0]
    tail = ''.join(command[1:])
    try:
        if head == 'halt':
            return 0x0000000000000000

        elif head == 'nop':
            return 0x1000000000000000

        elif head == 'rrmov':
            tempNum_1 = normalRegisters.get(tail.split(',')[0])  # rA
            tempNum_2 = normalRegisters.get(tail.split(',')[1])  # rB
            return 0x2000000000000000 ^ (tempNum_1 << 13 * 4) ^ (tempNum_2 << 12 * 4)

        elif head[0:4] == 'cmov':
            fn = judgements.get(head[4:])
            tempNum_1 = normalRegisters.get(tail.split(',')[0])  # rA
            tempNum_2 = normalRegisters.get(tail.split(',')[1])  # rB
            return 0x2000000000000000 ^ (fn << 14*4) ^ (tempNum_1 << 13 * 4) ^ (tempNum_2 << 12 * 4)

        elif head == 'irmov':
            tempNum_1 = 0xF
            tempNum_2 = normalRegisters.get(tail.split(',')[1])  # rB
            imm = int(tail.split(',')[0][2:], 16)  # 要注意把'0x'去掉
            if imm >= 2**48:
                logger.info('语句%s立即数过大，请修改您的指令。' % (commandLine))
                os.system('pause')
                exit()
            return 0x3000000000000000 ^ (tempNum_1 << 13 * 4) ^ (tempNum_2 << 12 * 4) ^ imm

        elif head == 'rmmov':
            tempNum_1 = normalRegisters.get(tail.split(',')[0])
            string = ','.join(tail.split(',')[1:])
            try:
                ad = addressingModes.get(string[0:3])
            except:
                logger.info('语句%s寻址方式错误' % (commandLine))
                os.system('pause')
                exit()
            return addressing_rm(ad, string[4: len(string) - 1], tempNum_1)

        elif head == 'mrmov':
            tempNum_1 = normalRegisters.get(
                tail.split(',')[len(tail.split(',')) - 1])
            string = ','.join(tail.split(',')[:(len(tail.split(',')) - 1)])
            try:
                ad = addressingModes.get(string[0:3])
            except:
                logger.info('语句%s寻址方式错误' % (commandLine))
                os.system('pause')
                exit()
            return addressing_mr(ad, string[4: len(string) - 1], tempNum_1)

        elif head in oprations:
            fn = oprations[head]
            if fn <= 0xB:
                tempNum_1 = normalRegisters.get(tail.split(',')[0])
                tempNum_2 = normalRegisters.get(tail.split(',')[1])
            else:
                tempNum_1 = normalRegisters.get(tail)
                tempNum_2 = 0
            return 0x6000000000000000 ^ (fn << 14 * 4) ^ (tempNum_1 << 13 * 4) ^ (tempNum_2 << 12 * 4)

        elif head[0] == 'j':
            fn = judgements.get(head[1:])
            tempNum = normalRegisters.get(tail)
            return 0x7000000000000000 ^ (fn << 14 * 4) ^ (0xF << 13 * 4) ^ (tempNum << 12 * 4)

        elif head == 'call':
            tempNum = normalRegisters.get(tail)
            return 0x8000000000000000 ^ (0xF << 13 * 4) ^ (tempNum << 12 * 4)

        elif head == 'ret':
            return 0x9000000000000000

        elif head == 'push':
            tempNum = normalRegisters.get(tail)
            return 0xA000000000000000 ^ (tempNum << 13 * 4) ^ (0xF << 12 * 4)

        elif head == 'pop':
            tempNum = normalRegisters.get(tail)
            return 0xB000000000000000 ^ (tempNum << 13 * 4) ^ (0xF << 12 * 4)

        else:
            logger.info('语句%s错误' % (commandLine))
            os.system('pause')
            exit()

    except:
        logger.info('语句%s错误' % (commandLine))
        os.system('pause')
        exit()
