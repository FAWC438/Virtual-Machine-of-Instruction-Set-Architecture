# 计算机组成原理作业

## 指令集系统模拟器实验报告

姓名 | 班级 |  学号  
-|-|-
凌国瀚 | 2018211318 | 2018213344 |
张北辰 | 2018211318 | 2018212258 |
张开元 | 2018211318 | 2018212229 |
范仲然 | 2018211318 | 2018212147 |

---

### 目录
<!-- TOC -->
>[一. 系统简介](#系统简介)
>
>[二. 运行环境与使用方法](#运行环境与使用方法)
>
>> 1. 运行环境
>>
>> 2. 使用方法——输入汇编指令
>>
>> 3. 使用方法——运行程序
>
>[三. 文件与主要变量简述](#文件与主要变量简述)
>
>> 1. 程序文件
>>
>> 2. 变量简述
>
>[四. 测试说明](#测试说明)
>
>> 1. 斐波那契数列
>>
>> 2. 递归求5的阶乘
>
>[五. 主要问题及其解决方案](#主要问题及其解决方案)
>
>> 1. 指令设计问题
>>
>> 2. 如何表示虚拟内存、通用寄存器和特殊寄存器
>
>[六. 团队分工](#团队分工)
>
>[七. 心得体会](#心得体会)
<!-- /TOC -->

---

### 系统简介

- 本指令集系统仿照x86-64指令集，实现的程序是一个支持数据传输、多种运算、堆栈操作、特权指令等功能的64位字长简单指令集系统虚拟机。该虚拟机设定的内存空间大小为 2**48 bit 。本程序使用Python编写，运用面向对象技术实现包括虚拟内存在内的大部分功能。

### 运行环境与使用方法

- 运行环境

  本程序源代码在Python3环境下均运行良好。该虚拟机的可执行 .exe 文件在Windows 10操作系统下均可正常运行。

- 使用方法——输入汇编指令

  首先在根目录找到**test.txt**文件，输入对应的汇编指令。格式类x86形式，具体支持的指令及其格式请查看根目录下**流程图与编码格式.pdf**文件，以下给出部分对应汇编指令示例，请注意对于其中的一些二地址指令如 `rrmov %rA, %rB`, 其中的%rA为源寄存器，%rB为目的寄存器。
  > **注意**：所有的逗号前后都***没有***空格，且不要输入多余空行
  
  ~~~x86asm
  nop                     # 空指令
  irmov 0x8,rdx           # 立即数-寄存器转移
  add rdx,rsp             # ALU加法运算
  pop rax                 # 出栈指令
  mrmov dir(0x3),rdx      # 内存-寄存器转移
  rmmov rdx,dir(0xfff)    # 寄存器-内存转移
  nop                     # 空指令
  halt                    # 特权休眠指令
  ~~~

  为了简化汇编语言，我们将寻址方式进行封装编码。在**test.txt**中使用不同寻址方式时请按照以下格式：

    >**注意**：在整个系统中，访问内存的操作***仅***允许在`mrmov`和`rmmov`两条指令中使用，其它指令只有访问寄存器的权限
    
    > **为什么舍弃立即寻址与寄存器寻址**？尽管设计了9种寻址方式，但在实际操作中，`rmmov`和`mrmov`的寄存器寻址操作完全可以被`rrmov`替代；同理，`irmov`也能替代立即寻址

  ~~~python
  #   寻址方式依次为：立即寻址（舍弃），直接寻址，
  #                   间接寻址，寄存器寻址（舍弃），
  #                   寄存器间接寻址，变址寻址，
  #                   相对寻址，基址寻址，
  #                   堆栈寻址
  addressingModes = {'imm': 0x0, 'dir': 0x1,
                   'ind': 0x2, 'reg': 0x3,
                   'inr': 0x4, 'mod': 0x5,
                   'rel': 0x6, 'bas': 0x7,
                   'sta': 0x8}
  #   未特别指明的寻址方式格式均为：
  MOED(DATA)
  eg. dir(0x3); inr(rax)
  #   变址寻址的格式为：
  mod(%Reg,$Imm)
  #   基址寻址格式为：
  bas(%Reg,$Imm)
  ~~~
  
  在**测试样例**文件夹中提供几个用于直接测试的样例及其说明，可以将其内容复制到根目录的**text.txt**文件中。

- 使用方法——运行程序
  
  运行该指令集系统模拟器，仅需直接点开根目录的**main.exe**即可。本程序也支持直接运行源代码运行，运行入口为**main.py**，但是由于本程序的一个依赖包`logging`不包含于Python标准库，因此需要使用pip加载该依赖包后才可直接运行源码。

  运行成功后，将在控制台显示每一周期的内存与寄存器变化，每2秒刷新一次。运行结束后可以在根目录的**log.txt**文件下阅读日志文件。

  > **温馨提示**：请在运行程序后将控制台保持全屏，否则当指令较多时，内容显示将不完全

### 文件与主要变量简述

- 程序文件

  - addressing.py

    处理所有的9种寻址方式，并通过不同方式返回最终地址

  - ALU.py

    运算器模块，提供14种不同的运算操作并同时对条件码寄存器进行更新

  - call.py

    函数调用与返回指令模块，通常配合堆栈指令应用于函数调用或递归操作

  - init.py

    提供程序主要全局变量与实例对象的声明，并调用主要的依赖包

  - IO_encode.py

    IO模块依赖包，主要功能为将输入文件中作为字符串的指令转换为64位2进制编码
  
  - IO.py

    IO模块，功能为将文件中的字符串指令转化为2进制编码并存入指定内存位置

  - jump.py

    跳转与条件跳转模块，主要执行各种跳转指令，并改变PC寄存器的值
  
  - main.py

    主函数与译码器模块，实现程序入口与编码的译码工作，调用相应的模块执行指令。同时兼顾控制台/日志输出功能，能够实时监控虚拟机的运行情况

  - memory.py

    内存抽象类的定义模块，定义了内存的抽象类及其函数，便于各个模块的调用。使用面向对象技术和Python的字典数据结构，一定程度上模拟了现代计算机的虚拟内存功能

  - other.py

    特权指令与空指令模块，能够对状态寄存器进行改变
  
  - register.py

    寄存器抽象类及其子类的定义模块，定义了所有通用寄存器和特殊寄存器的抽象类，便于多次调用

  - stack.py

    堆栈操作模块，提供压栈与出栈的方法。本程序中，栈指针指向内存最后一个地址，堆栈的范围是`0xf00000000000-0xfffffffffffffffe`。每个周期都会清楚出栈内容

  - transport.txt

    转移操作与条件转移操作模块，实现数据转移的功能。在所有模块中，只有这个模块有权限访问内存。

  - log.txt

    日志文件，配有时间戳，可以查看控制台输出的所有信息

  - test.txt

    指令输入位置，将待执行的指令存放于此才可正常运行程序。如果要执行main.exe，必须将该文件与main.exe放于同一个目录下

  - mian.exe

    可执行文件。将该文件与test.txt放于同一个目录下才可正常运行

- 变量简述
  
  ~~~python
  commandContent = {}   # 存储指令的字符串格式以便输出
  memory = Memory()     # 内存对象实例
  registers = [Register() for i in range(16)]   # 15个通用寄存器+1个立即数指示器（0xF）
  psw = Psw()           # 条件码寄存器
  pc = PC()             # 程序计数器
  xReg = Register()     # ALU临时寄存器
  yReg = Register()     # ALU临时寄存器
  state = State()       # 状态寄存器
  AR = ARegister()      # 地址寄存器
  IR = IRegister()      # 指令寄存器
  DR = DRegister()      # 缓冲寄存器
  ~~~
  
  15个通用寄存器名称具体见**流程图与编码格式.pdf**，需要注意的是通用寄存器第0x4个，即rsp栈指针寄存器，其总是指向内存最后一块地址

### 测试说明

- 斐波那契数列

  可直接于**text.txt**运行的代码如下：

  ~~~x86asm
  irmov 0x1,rbx
  irmov 0x1,rcx
  irmov 0x7,rax
  irmov 0x3,rdx
  irmov 0x1000,r8
  cmp rdx,rax
  irmov 0x10,r14
  jl r14
  rrmov rcx,r14
  add rbx,rcx
  rmmov rcx,inr(r8)
  inc r8
  rrmov r14,rbx
  inc rdx
  irmov 0x5,r14
  jmp r14
  halt
  ~~~

  注释说明如下：

  ~~~x86asm
  .main
  # rbx, rcx用来存动态规划状态压缩后的两个数
  irmov 0x1, rbx  # f_1
  irmov 0x1, rcx  # f_2
  irmov 0x7, rax  # 求斐波那契数列第7项
  irmov 0x3, rdx  # 迭代的i
  irmov 0x1000,r8 # 初始写入地址

  .loop
  cmp rdx, rax
  jl xxx              # i > n 跳出循环
  rrmov rcx, r14
  add rbx, rcx        # fn = f_(n - 1) + f_(n - 2)
  rmmov rcx, inr(r8)  # 结果存放位置
  inc r8              # 每次存放的地址自增1
  rrmov r14, rbx
  inc rdx
  jmp .loop

  .xxx
  halt
  ~~~

  该样例测试计算斐波那契数列，计算上限为13，分别存储在内存的`0x1000 - 0x1004`位置。
- 递归求5的阶乘

  可直接于text.txt运行的代码如下：

  ~~~x86asm
  irmov 0x5, rdi
  irmov 0x6, r14
  call r14
  rmmov rax, dir(0x1000)
  halt

  push rbx
  irmov 0x8, rbx
  sub rbx, rsp
  irmov 0x0, rbx
  cmp rbx, rdi
  irmov 0x17, r14
  je r14
  push rdi
  irmov 0x1, rbx
  sub rbx, rdi
  irmov 0x6, r14
  call r14
  pop rdi
  imul rdi, rax
  irmov 0x18, r14
  jmp r14

  irmov 0x1, rax
  irmov 0x8, rbx
  add rbx, rsp
  pop rbx
  ret
  ~~~

  注释说明如下：

  ~~~x86asm
  .main
  # rbx用于运算时临时储存立即数，被调用者保护；r14用于跳转/调用无保护
  irmov 0x5, rdi          # 参数为5
  irmov .fact, r14
  call r14
  rmmov rax, dir(0x1000)  # 结果存放位置
  halt

  .fact
  push rbx
  irmov 0x8, rbx
  sub rbx, rsp
  irmov 0x0, rbx
  cmp rbx, rdi
  irmov .L2, r14
  je r14                  #if(rdi == 0)
  push rdi
  irmov 0x1, rbx
  sub rbx, rdi
  irmov .fact, r14
  call r14
  pop rdi
  imul rdi, rax
  irmov .L3, r14
  jmp r14

  .L2
  irmov 0x1, rax
  .L3
  irmov 0x8, rbx
  add rbx, rsp
  pop rbx
  ret
  ~~~

  该测试样例利用堆栈实现递归功能，从而计算出5的阶乘，结果存储在内存的`0x1000`位置

### 主要问题及其解决方案

- 指令设计问题

  该项目之初，本团队考虑过多种指令编码格式作为原型，包括MIPS、IBM系列等，但是最后还是选择了较为熟悉的x86指令集。主要原因是在之前的计算机系统基础中本团队较为深入的了解了该指令集系统，且教材《深入了解计算机系统》对设计x86指令集系统有较为详尽的讲解。

  然而在着手设计时遭遇了很多问题，例如：

  - 每种指令访问内存时都需要寻址，指令集系统过于庞大，且多种寻址方式下译码器难以运作

  - 如何合理地编码以表明正确的寻址方式和数据流向

  为了解决这个问题，本团队对指令集进行了简化，主要内容如下

  - 提高访问内存的门槛，使得特定传送指令才能直接访问内存，其它指令只能间接通过寄存器访问。

  - 固定48位为内存地址，而剩余的16位将控制位和寄存器位灵活应用令编码更加简洁合理。例如，将原本的16个通用寄存器的最后一个的内容设为全1，作为表示立即数的标志。

- 如何表示虚拟内存、通用寄存器和特殊寄存器

  对于内存和寄存器，本团队设计之初将他们设为全局变量。然而在慢慢实现时发现了不少问题：

  - 作为全局变量的内存和寄存器容易发生一些数据上的错误，并且相关函数冗长重复。

  - 以全局变量来调用内存和寄存器，无法体现指令集系统中的总线结构，更无法体现虚拟内存的映射机制。

  - 2**48 bit的内存大小过于庞大，全局变量难以定义。

  于是本团队决定利用Python语言的优势解决这些问题：
  - 使用面向对象技术封装内存和寄存器类与他们的方法，并令众多特殊寄存器作为子类，依次在**init.py**中实例化。

  - 利用Python中的特殊数据结构**字典**来模拟虚拟内存，只有有意义的内存才会被映射，节省了空间的同时也实现了使用虚拟内存的要求。

### 团队分工

- 凌国瀚

  负责流程图绘制与说明文档撰写，编写IO模块、main函数和译码器模块、

- 张北辰

  负责流程图设计与程序测试与测试样例设计，编写传送/条件传送模块、跳转/条件跳转模块

- 张开元

  负责流程图设计与程序测试与测试样例设计，编写栈指令模块、特权指令和空指令模块

- 范仲然

  负责流程图设计，编写ALU模块

### 心得体会

- 凌国瀚

  通过这次指令集系统作业，我通过团队协作学习到了指令集流程图绘制的技巧与困难，定位每个时刻数据的流向不是一件容易的工作；我同时也在编写IO模块时得到了锻炼，该模块对于字符串匹配和二进制位操作的要求较高，花费了我大量的时间，幸而最后成功完成了任务。本次作业让我积累了团队协作的经验，提升了Python程序设计技巧，了解了指令如何在计算机中发挥作用，并且对CPU中的数据通路、时序信号、内存寻址等概念有了更深的理解。

- 张北辰

  本次指令系统实验除了让我对计算机组成、指令系统设计、数据通路有了更清晰的认识之外，还让我有了很多其他方面的收获。

  小组内采用面向对象的设计方式进行指令系统的模拟，相对贴合物理硬件通过数据通路在不同的存储器之间交换数据的场景，通过这样的模拟让我更清晰地认识到了封装在程序设计中的优越性。同时，在团队协作进行编码的过程中，曾经出现过对队友的代码功能理解不清导致误用的经历，这让我明白了设计和撰写清晰明了的接口文档的重要性。

  在设计汇编测试样例的过程中，通过分支跳转结构的书写，我理解了目前我们自己模拟的CPU行为的低效，同时也理解了CPU流水线优化和分支预测功能的优越性。

  在寻址方式的设计中，我一开始将访存取值也纳入了这一过程，后来发现这种包揽反而会增加译码器调用的困难，可见在进行功能设计的时候不同队友就需要沟通，同时自己也应该周全地考虑合作者的需求。

- 张开元

  这次指令系统实验使我对计算机组成和指令系统设计有了更深刻的认识，最重要的一点是指令的设计需要协调考虑软件开发者的需求和基础硬件的功能，在前期流程图设计中，为了简化译码逻辑，我们将指令设计成64位定长指令，这种方式有很大的代价，产生了大量的无用数据占据内存；我们还将调用和跳转指令的寻址方式固定为寄存器间接寻址，导致后期写测试样例的时候需要牺牲一个通用寄存器用于寻址。因此，我认识到：一个优秀的指令系统，应当对软件“友好”，对硬件“负责”。
  
  除此之外，我在实验中积累了团队协作的经验，学习了面向对象编程的思想，提升了python语言的使用和理解。测试样例中使用汇编语言编程，加深了我对机器指令和汇编语言之间关系的理解。

- 范仲然

  这次指令集系统实验加深了我对计算机组成原理和指令集系统的理解。
  
  此次实验小组商讨决定采用python语言，而我之前没有接触过python编程和面向对象编程，因此学习python语言和面向对象编程原则耗费了我大量的时间。
  
  本次实验中我负责编写ALU模块的代码。这部分代码逻辑难度不大，但由于其在程序中需要被频繁的调用，需要考虑鲁棒性和规范性以方便对接。此外，由于python的变量过于灵活，因此考虑对运算溢出等情况的处理也花费了一些时间。
