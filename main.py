from init import *
from IO import io
from IO_encode import normalRegisters

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


if __name__ == "__main__":
    io()
    clock = 0
    registers[4].data = 0xffffffffffff
    while True:

        pc.readData()
        AR.writeData()
        try:
            memory.readData(AR, DR)
        except:
            logger.info('PC：'+str(hex(pc.data))+'指向空地址...')
            os.system('pause')
            exit()
        DR.readData()
        IR.writeData()

        os.system('cls')
        logger.info(
            '-----------------------------------------------------------\n')
        logger.info('指令周期为：%d' % (clock))
        logger.info('PC：' + str(hex(pc.data)))
        logger.info('AR：' + str(hex(AR.data)))
        logger.info('IR：' + str(hex(IR.data)))
        logger.info('DR：' + str(hex(DR.data)))
        regName = list(normalRegisters.keys())

        string  = ''
        for i in range(15):
            if(i % 4 == 0 and i != 0):
                logger.info(string)
                string = ''
            string = string + "%3s: %-16s\t" % (regName[i], str(hex(registers[i].data)))
        logger.info(string)

        logger.info('当前执行指令为：'+commandContent[pc.data])
        for i in list(memory.memory.keys()):
            if (i >= 0xf00000000000) and (i < registers[4].data):
                memory.memory.pop(i)
        logger.info('------------以下是所有内存的情况------------')
        for i in sorted(memory.memory.items(), key=lambda item: item[0], reverse=False):
            logger.info('地址：'+str(hex(i[0]))+'   数据：'+str(hex(i[1])))
        logger.info('------------以上是所有内存的情况------------')

        logger.info(
            '-----------------------------------------------------------\n')

        pc.inc()
        A = IR.getRegA()
        B = IR.getRegB()
        if IR.getInsType() == 0x0:
            halt(state)

        elif IR.getInsType() == 0x1:
            nop()

        elif IR.getInsType() == 0x2:
            if IR.getFn() == 0x0:
                rrMov(registers[A], registers[B])
            elif IR.getFn() <= 0x6:
                cMov(registers[A],
                     registers[B], psw, IR.getFn())
            else:
                state.setINS()

        elif IR.getInsType() == 0x3:
            irMov(IR.getImm(), registers[B])

        elif IR.getInsType() == 0x4:
            # if IR.getAddType() == 0x0:
            #    finalAddress = IR.getImm
            if IR.getAddType() == 0x1:
                addDir(AR, DR, memory, IR.getImm())
            elif IR.getAddType() == 0x2:
                addIndir(AR, DR, memory, IR.getImm())
            # elif IR.getAddType() == 0x3:
            #     addReg(registers[B])
            #     finalAddress = Register.BUS
            elif IR.getAddType() == 0x4:
                addRegIndir(registers[B], AR, DR, memory)
            elif IR.getAddType() == 0x5:
                addIndex(registers[B], IR.getImm(),
                         AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x6:
                addRelate(pc, IR.getImm(), AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x7:
                addBase(registers[B], IR.getImm(),
                        AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x8:
                addStack(registers[4], AR, DR, memory)
            else:
                state.setINS()
            rmMov(registers[A], AR, DR, memory)

        elif IR.getInsType() == 0x5:
            # if IR.getAddType() == 0x0:
            #     finalAddress = addImm(IR.getImm)
            if IR.getAddType() == 0x1:
                addDir(AR, DR, memory, IR.getImm())
            elif IR.getAddType() == 0x2:
                addIndir(AR, DR, memory, IR.getImm())
            # elif IR.getAddType() == 0x3:
            #     addReg(registers[A])
            #     finalAddress = Register.BUS
            elif IR.getAddType() == 0x4:
                addRegIndir(registers[A], AR, DR, memory)
            elif IR.getAddType() == 0x5:
                addIndex(registers[A], IR.getImm(),
                         AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x6:
                addRelate(pc, IR.getImm(), AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x7:
                addBase(registers[A], IR.getImm(),
                        AR, DR, memory, xReg, yReg, psw)
            elif IR.getAddType() == 0x8:
                addStack(registers[4], AR, DR, memory)
            else:
                state.setINS()
            mrMov(registers[B], AR, DR, memory)

        elif IR.getInsType() == 0x6:
            if IR.getFn() == 0x0:
                ALU_cmp(registers[A], registers[B], psw)
            elif IR.getFn() == 0x1:
                add(registers[A], registers[B], psw)
            elif IR.getFn() == 0x2:
                sub(registers[A], registers[B], psw)
            elif IR.getFn() == 0x3:
                imul(registers[A], registers[B], psw)
            elif IR.getFn() == 0x4:
                div(registers[A], registers[B], psw)
            elif IR.getFn() == 0x5:
                bit_xor(registers[A], registers[B], psw)
            elif IR.getFn() == 0x6:
                bit_or(registers[A], registers[B], psw)
            elif IR.getFn() == 0x7:
                bit_and(registers[A], registers[B], psw)
            elif IR.getFn() == 0x8:
                sal(registers[A], registers[B], psw)
            elif IR.getFn() == 0x9:
                shl(registers[A], registers[B], psw)
            elif IR.getFn() == 0xA:
                sar(registers[A], registers[B], psw)
            elif IR.getFn() == 0xB:
                shr(registers[A], registers[B], psw)
            elif IR.getFn() == 0xC:
                inc(registers[A], psw)
            elif IR.getFn() == 0xD:
                dec(registers[A], psw)
            else:
                state.setINS()

        elif IR.getInsType() == 0x7:
            if IR.getFn() == 0x0:
                jmp(registers[B], pc, AR, DR, memory)
            elif IR.getFn() <= 0x6:
                cjmp(registers[B], pc, AR,
                     DR, memory, psw, IR.getFn())
            else:
                state.setINS()
            # pc.data -= 1

        elif IR.getInsType() == 0x8:
            call(registers[4], AR, DR, memory, pc, registers[B])

        elif IR.getInsType() == 0x9:
            ret(registers[4], AR, DR, memory, pc)

        elif IR.getInsType() == 0xA:
            push(registers[A], registers[4], AR, DR, memory)

        elif IR.getInsType() == 0xB:
            pop(registers[A], registers[4], AR, DR, memory)

        else:
            state.setINS()

        if ((registers[4].data >= 2 ** 48 or registers[4].data < 0) or
                (pc.data >= registers[4].data or pc.data < 0)):
            state.setADR()

        if state.getState() == 1:  # HLT
            logger.info('CPU正常进入待机状态。【按下R键重启，按下ESC键关机】')
        elif state.getState() == 2:  # ADR
            logger.info('发生地址错误，请检查程序！【按下R键重启，按下ESC键关机】')
        elif state.getState() == 3:  # INS
            logger.info('发生指令错误，请检查程序！【按下R键重启，按下ESC键关机】')
        if state.getState() != 0:
            ch = getch()
            while (ch[0] != 0x52) and (ch[0] != 0x72) and (ch[0] != 0x1B):
                ch = getch()
            if (ch[0] == 0x52) or (ch[0] == 0x72):
                memory.clearMemory()
                os.system('cls')
                io()
                clock = 0
                registers[4].data = 0xffffffffffff
                state.setAOK()
            elif ch[0] == 0x1B:
                break

        time.sleep(2)
        clock += 1

    os.system('cls')
    logger.info('程序结束，请到目录下log.txt文件查看运行日志')
    os.system('pause')
