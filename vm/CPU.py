class CPU:
    ip = 0  # instruction pointer
    fp = -1  # frame pointer
    cpu_stack = list()  # operation stack
    cpu_stack_arg = list()  # argument stack
    last_op = None  # last executed opCode
    panic = False  # is the cpu in a faulted state?

    __memory = None
    __memory_size = 0
    __memory_used = 0

    def __init__(self, memory_size):
        self.__memory = [00] * memory_size
        self.__memory_size = memory_size

        '''
        each instruction has three attributes:
            op_code -> operation code
            param_count -> number of parameters taken from memory
            op -> function pointer
            
        During function calls,
        the caller is responsible for pushing the arguments onto the stack
        and then cleaning the stack after the function returns aka cdecl convention
        '''
        self.instructions = [
            {"mnemonic": "nop",     "param_count": 0,       "op": self.nop},         # 0
            {"mnemonic": "add",     "param_count": 0,       "op": self.add},         # 1
            {"mnemonic": "sub",     "param_count": 0,       "op": self.sub},         # 2
            {"mnemonic": "mul",     "param_count": 0,       "op": self.mul},         # 3
            {"mnemonic": "div",     "param_count": 0,       "op": self.div},         # 4
            {"mnemonic": "mod",     "param_count": 0,       "op": self.mod},         # 5
            {"mnemonic": "dup",     "param_count": 0,       "op": self.dup},         # 6
            {"mnemonic": "push",    "param_count": 1,       "op": self.push},        # 7
            {"mnemonic": "pop",     "param_count": 0,       "op": self.pop},         # 8
            {"mnemonic": "swap",    "param_count": 0,       "op": self.swap},        # 9
            {"mnemonic": "jmptos",  "param_count": 0,       "op": self.jmptos},      # 10
            {"mnemonic": "jmp",     "param_count": 1,       "op": self.jmp},         # 11
            {"mnemonic": "beq",     "param_count": 1,       "op": self.beq},         # 12 ==
            {"mnemonic": "bne",     "param_count": 1,       "op": self.bne},         # 13 !=
            {"mnemonic": "bgt",     "param_count": 1,       "op": self.bgt},         # 14 >
            {"mnemonic": "bgte",    "param_count": 1,       "op": self.bgte},        # 15 >=
            {"mnemonic": "blt",     "param_count": 1,       "op": self.blt},         # 16 <
            {"mnemonic": "blte",    "param_count": 1,       "op": self.blte},        # 17 <=
            {"mnemonic": "ovr",     "param_count": 0,       "op": self.ovr},
            {"mnemonic": "dup2",    "param_count": 0,       "op": self.dup2},
            {"mnemonic": "ovr2",    "param_count": 0,       "op": self.ovr2},
            {"mnemonic": "popprev", "param_count": 1,       "op": self.popprev},
            {"mnemonic": "call",    "param_count": 1,       "op": self.call},
            {"mnemonic": "ret",     "param_count": 0,       "op": self.ret},
            {"mnemonic": "ldarg",   "param_count": 1,       "op": self.ldarg},
            {"mnemonic": "inc",     "param_count": 0,       "op": self.inc},
            {"mnemonic": "dec",     "param_count": 0,       "op": self.dec},
            {"mnemonic": "hlt",     "param_count": 0,       "op": self.halt},        # 1
        ]

    def check_memory_bound(self, position):
        if position > self.__memory_size:
            raise IndexError("Memory size: {0}, Position requested: {1}".format(self.__memory_size, position))

    def memory_store(self, position, data):
        self.check_memory_bound(position)
        self.__memory[position] = data

    def memory_load(self, position):
        self.check_memory_bound(position)
        return self.__memory[position]

    def get_ip(self):
        return self.ip

    def get_fp(self):
        return self.fp

    def load_program(self, program):
        if len(program) > self.__memory_size:
            raise OverflowError("Program (size: {0}) is too big for the memory (size: {1})"
                                .format(len(program), self.__memory_size))
        for data in program:
            self.__memory[self.__memory_used] = data
            self.__memory_used += 1

    def nop(self):
        pass

    def add(self):
        self.cpu_stack.append(self.cpu_stack.pop() + self.cpu_stack.pop())

    def sub(self):
        self.cpu_stack.append(self.cpu_stack.pop() - self.cpu_stack.pop())

    def mul(self):
        self.cpu_stack.append(self.cpu_stack.pop() * self.cpu_stack.pop())

    def div(self):
        self.cpu_stack.append(self.cpu_stack.pop() // self.cpu_stack.pop())

    def mod(self):
        self.cpu_stack.append(self.cpu_stack.pop() % self.cpu_stack.pop())

    def push(self, value):
        self.cpu_stack.append(value)

    def pop(self):
        self.cpu_stack.pop()

    def dup(self):
        self.cpu_stack.append(self.cpu_stack[-1])

    def dup2(self):
        self.cpu_stack += [self.cpu_stack[-2], self.cpu_stack[-1]]

    # pops the top of the stack and jumps to that, provided that its a valid address
    def jmptos(self):
        offset = self.cpu_stack.pop()
        self.check_memory_bound(offset)
        self.ip = offset - 1  # -1 because the execution unit automatically adds 1 to ip after each instruction

    def jmp(self, address):
        self.check_memory_bound(address)
        self.ip = address - 1  # -1 because the execution unit automatically adds 1 to ip after each instruction

    # >>> all conditional branches instructions pop top two elements for comparison
    # if the branching statement yields false then the values are restored to stack
    def beq(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a == b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def bne(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a != b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def bgt(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a > b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def bgte(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a >= b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def blt(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a < b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def blte(self, address):
        a = self.cpu_stack.pop()
        b = self.cpu_stack.pop()
        if a <= b:
            self.jmp(address)
        else:
            self.cpu_stack += [b, a]

    def ovr(self):
        self.cpu_stack.append(self.cpu_stack[-2])

    def ovr2(self):
        self.cpu_stack.append(self.cpu_stack[-3])

    def popprev(self, n):
        if n > len(self.cpu_stack) - 1:
            raise SystemError("Popprev requested: {0}. Available items: {1}".format(n, len(self.cpu_stack)))
        tos = self.cpu_stack.pop()
        while n > 0:
            self.cpu_stack.pop()
            n -= 1
        self.cpu_stack.append(tos)

    def call(self, address):
        self.cpu_stack.append(self.fp)
        self.cpu_stack.append(self.ip + 1)  # return address
        self.fp = len(self.cpu_stack)
        self.jmp(address)

    def ret(self):
        tos = self.cpu_stack.pop()
        del self.cpu_stack[self.fp:]
        self.jmp(self.cpu_stack.pop())  # set instruction pointer to return address
        self.fp = self.cpu_stack.pop()  # restore stack pointer
        self.cpu_stack.append(tos)  # push the return value back to stack for the caller

    def ldarg(self, arg_number):
        if self.fp == -1:
            raise SystemError("ldarg called outside a function")
        self.cpu_stack.append(
            self.cpu_stack[(self.fp-2)-arg_number]
        )

    def inc(self):
        self.cpu_stack[-1] += 1

    def dec(self):
        self.cpu_stack[-1] -= 1

    def halt(self):
        print("\n\nTOS :", self.cpu_stack.pop())
        self.panic = True

    def swap(self):
        if len(self.cpu_stack) < 2:
            return
        self.cpu_stack[-1], self.cpu_stack[-2] = self.cpu_stack[-2], self.cpu_stack[-1]

    def execute(self):
        while self.ip < self.__memory_size and not self.panic:
            ins = self.instructions[self.memory_load(self.ip)]
            params = []
            if ins["param_count"] > 0:
                for i in range(1, ins["param_count"]+1):
                    params.append(self.memory_load(self.ip+i))
                self.ip += ins["param_count"]
            ins["op"](*params)
            self.ip += 1
            #print(self.ip-ins["param_count"], "\t:", ins["mnemonic"] + " ", *params,
            #      "\t" if len(params) > 0 else "\t\t",
            #     self.cpu_stack)
