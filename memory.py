class Memory(object):
    def __init__(self):
        self.memory = {}    # 为啥不是self.data = {}
        self.addressBus = 0
        self.dataBus = 0

    def readData(self, ARegister, DRegister):
        """
        从地址寄存器读取地址后将对应数据放到缓冲寄存器
        :param ARegister: 地址寄存器
        :param DRegister: 缓冲寄存器
        :return:
        """
        ARegister.readFromMeomory(self)
        self.getMemory()
        # 改成DR
        DRegister.writeFromMemory(self)

    def writeData(self, ARegister, DRegister):
        """
        从地址寄存器读取地址后将缓冲寄存器数据写到内存中
        :param ARegister: 地址寄存器
        :param DRegister: 缓冲寄存器
        :return:
        """
        ARegister.readFromMeomory(self)
        DRegister.readFromMemory(self)
        self.memory[self.addressBus] = self.dataBus

    def getMemory(self):
        self.dataBus = self.memory[self.addressBus]

    def clearMemory(self):
        self.memory.clear()