from register import Register, Psw

cut_to_64 = 0xffffffffffffffff


def update_psw(temp, res, psw: Psw):
    psw.ZF = res == 0
    psw.SF = res < 0
    psw.OF = res != temp


def inc(rB: Register, psw: Psw):
    temp = rB.data + 1
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def dec(rB: Register, psw: Psw):
    temp = rB.data - 1
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def add(rA: Register, rB: Register, psw: Psw):
    temp = rB.data + rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def sub(rA: Register, rB: Register, psw: Psw):
    temp = rB.data - rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def imul(rA: Register, rB: Register, psw: Psw):
    temp = rB.data * rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def div(rA: Register, rB: Register, psw: Psw):
    temp = rB.data // rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def bit_xor(rA: Register, rB: Register, psw: Psw):
    temp = rB.data ^ rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def bit_or(rA: Register, rB: Register, psw: Psw):
    temp = rB.data | rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def bit_and(rA: Register, rB: Register, psw: Psw):
    temp = rB.data & rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def sal(rA: Register, rB: Register, psw: Psw):
    temp = rB.data << rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def shl(rA: Register, rB: Register, psw: Psw):
    temp = rB.data << rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)


def sar(rA: Register, rB: Register, psw: Psw):
    temp = rB.data >> rA.data
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)



def shr(rA: Register, rB: Register, psw: Psw):
    temp = (rB.data >> rA.data) & (cut_to_64 >> rA.data)
    res = temp & cut_to_64
    rB.data = res
    update_psw(temp, res, psw)



def ALU_cmp(rA: Register, rB: Register, psw: Psw):
    temp = rB.data - rA.data
    res = temp & cut_to_64
    update_psw(temp, res, psw)
