from memory import Memory

class Register(object):
    BUS = 0

    def __init__(self):
        self.data = 0

    def readData(self):
        """
        将寄存器中的数据/地址放到总线上
        """
        Register.BUS = self.data

    def writeData(self):
        """
        将总线上的数据/地址给寄存器
        """
        self.data = Register.BUS


class Psw(Register):
    def __init__(self):
        self.ZF = 0
        self.SF = 0
        self.OF = 0
    # if((SF^OF)|ZF):

    def lessEqual(self):
        return ((self.SF ^ self.OF) | self.ZF)

    # if(SF^OF):

    def less(self):
        return (self.SF ^ self.OF)

    # if(ZF):

    def equal(self):
        return self.ZF

    # if(~ZF):

    def unequal(self):
        return ~self.ZF

    # if(~(SF^OF)):

    def largeEqual(self):
        return ~ (self.SF ^ self.OF)

    # if(~(SF^OF)&~ZF):

    def large(self):
        return ~(self.SF ^ self.OF) & ~self.ZF


class PC(Register):
    def inc(self):
        self.data += 1

class ARegister(Register):
    def readFromMeomory(self, memory: Memory):
        """
        将AR中的地址放到地址总线上
        :param memory:
        :return:
        """
        memory.addressBus = self.data

class DRegister(Register):
    def writeFromMemory(self, memory: Memory):
        """
        将数据总线的数据给DR
        :param memory:
        :return:
        """
        self.data = memory.dataBus

    def readFromMemory(self, memory: Memory):
        """
        将DR中的数据放大数据总线上
        :param memory:
        :return:
        """
        memory.dataBus = self.data

class IRegister(Register):
    def getImm(self):
        """
        将IR中指令的立即数/直接地址/偏移量字段送给控制器
        """
        return self.data & 0x0000ffffffffffff
    
    def getInsType(self):
        """
        将IR中指令的指令类型字段送给控制器
        """
        return (self.data & 0xf000000000000000) >> 60

    def getAddType(self):
        """
        将IR中指令的寻址方式字段送给控制器
        注意: 该字段根据指令类型不同, 也可能为功能字段, IR寄存器对此不作区分
        """
        return (self.data & 0x0f00000000000000) >> 56

    def getFn(self):
        """
        将IR中指令的功能字段送给控制器
        注意: 该字段根据指令类型不同, 也可能为寻址方式字段, IR寄存器对此不作区分
        """
        return (self.data & 0x0f00000000000000) >> 56

    def getRegA(self):
        """
        将IR中寄存器A字段送给控制器
        """
        return (self.data & 0x00f0000000000000) >> 52

    def getRegB(self):
        """
        将IR中寄存器B字段送给控制器
        """
        return (self.data & 0x000f000000000000) >> 48

class State(Register):

    def __init__(self):
        self.data = 0
    
    def getState(self):
        return (self.data & 0x000000000000000f)

    def setAOK(self):
        self.data = (self.data & 0xfffffffffffffff0) | 0x0
    
    def setHLT(self):
        if(self.getState() == 0):
            self.data = (self.data & 0xfffffffffffffff0) | 0x1
    
    def setADR(self):
        self.data = (self.data & 0xfffffffffffffff0) | 0x2

    def setINS(self):
        self.data = (self.data & 0xfffffffffffffff0) | 0x3