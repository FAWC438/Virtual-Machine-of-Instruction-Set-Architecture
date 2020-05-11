from init import *
from IO_encode import encodeCommand

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


def io():
    logger.info('请输入指令起始十进制PC地址（默认为0）:')
    temp = input()
    if temp.isdecimal():
        pointer = int(temp)
    else:
        pointer = 0

    pc.data = pointer
    if pc.data >= 2**48 or pc.data < 0:
        logger.info('地址越界！请输入正确地址...')
        os.system('pause')
        exit()
    else:
        logger.info('指令起始PC地址为0x%x', pc.data)

    # 输入文件为当前目录的test.txt
    with open(r'test.txt', 'r') as in_file:
        s = in_file.readline()
        while s != '':
            s = s.strip().lower()   # 去除首尾空格，全变为小写
            if pointer >= 2**48:
                logger.info('指令内容过多，内存空间不足！')
                os.system('pause')
                exit()
            if s[0:2] == '0x':
                memory.memory[pointer] = int(s[2:], 16)
            elif len(s) > 0:
                memory.memory[pointer] = encodeCommand(s)
                commandContent[pointer] = s
            pointer += 1
            s = in_file.readline()
        in_file.close()
    logger.info('指令读取完成！')
    time.sleep(2)
