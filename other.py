from register import State

def nop():
    pass

def halt(state: State):
    """
    停机指令, 执行后虚拟机进入待机状态
    :param state:
    :return:
    """
    state.setHLT()