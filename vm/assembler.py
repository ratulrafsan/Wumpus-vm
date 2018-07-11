class assembler:
    def __init__(self):
        self.instructions = {
            "nop":      {"opcode": 0,  "param_count": 0},
            "add":      {"opcode": 1,  "param_count": 0},
            "sub":      {"opcode": 2,  "param_count": 0},
            "mul":      {"opcode": 3,  "param_count": 0},
            "div":      {"opcode": 4,  "param_count": 0},
            "mod":      {"opcode": 5,  "param_count": 0},
            "dup":      {"opcode": 6,  "param_count": 1},
            "push":     {"opcode": 7,  "param_count": 1},
            "pop":      {"opcode": 8,  "param_count": 0},
            "swap":     {"opcode": 9,  "param_count": 0},
            "jumptos":  {"opcode": 10, "param_count": 0},
            "jmp":      {"opcode": 11, "param_count": 1},
            "beq":      {"opcode": 12, "param_count": 1},
            "bne":      {"opcode": 13, "param_count": 1},
            "bgt":      {"opcode": 14, "param_count": 1},
            "bgte":     {"opcode": 15, "param_count": 1},
            "blt":      {"opcode": 16, "param_count": 1},
            "blte":     {"opcode": 17, "param_count": 1},
            "ovr":      {"opcode": 18, "param_count": 0},
            "popprev":  {"opcode": 19, "param_count": 1},
            "call":     {"opcode": 20, "param_count": 1},
            "ret":      {"opcode": 21, "param_count": 0},
            "ldarg":    {"opcode": 22, "param_count": 1},
            "inc":      {"opcode": 23, "param_count": 0},
            "dec":      {"opcode": 24, "param_count": 0},
            "debug":    {"opcode": 25, "param_count": 1},
            "hlt":      {"opcode": 26, "param_count": 0}
        }

    #[line for line in open(file,r)]
    def assemble(self, code):
        bytecode = []
        jump_table = {}
        for line_number, line in enumerate(code):
            __buffer = ""
            i = 0
            expecting_arg = False
            expected_arg_count = 0
            args_found = 0
            expecting_arg_for = ""
            while i < len(line):
                # comment check
                if line[i] == '-':
                    if i+1 < len(line):
                        # is it a comment? then go to next line
                        if line[i+1] == '-':
                            break
                        # is a negative sign for a number?
                        elif line[i+1].isdigit():
                            # are we expecting an argument? if not then throw error
                            if not expecting_arg:
                                __buffer += line[i] + line[i+1]
                                print(__buffer, "Unexpected argument/number. line: ", line_number)
                                exit(0)
                            else:
                                __buffer += line[i] + line[i + 1]
                                args_found += 1
                                bytecode.append(int(__buffer))
                                i += 2
                                if expected_arg_count == args_found:
                                    expecting_arg = False
                                    expected_arg_count = args_found = 0
                                    expecting_arg_for = ""
                        else:
                            print(line[i], "just a - sign? line: ", line_number)
                            exit(0)
                elif line[i].isdigit():
                    #  are we expecting an argument?
                    if not expecting_arg:
                        __buffer += line[i]
                        print(__buffer, "Unexpected argument/number. line: ", line_number)
                        exit(0)
                        i += 2
                    else:
                        __buffer += line[i]
                        args_found += 1
                        if i+1 < len(line):
                            i += 1
                            if not line[i].isspace():
                                while (i < len(line)) and line[i].isdigit():
                                    __buffer += line[i]
                                    i += 1
                        i += 1
                        bytecode.append(int(__buffer))
                        if expected_arg_count == args_found:
                            expecting_arg = False
                            expected_arg_count = args_found = 0
                            expecting_arg_for = ""
                elif line[i].isalpha():
                    __buffer += line[i]
                    i += 1
                    if i < len(line):
                        if not line[i].isspace():
                            while i < len(line) and line[i].isalnum():
                                __buffer += line[i]
                                i += 1
                    if __buffer.isupper():
                        if __buffer in jump_table.keys():
                            print("Multiple declaration of", __buffer, ".Line: ", line_number)
                            exit(0)
                        jump_table[__buffer] = len(bytecode)
                        i += 1
                        continue
                    try:
                        ins = self.instructions[__buffer]
                        if ins["param_count"] > 0:
                            expecting_arg = True
                            expecting_arg_for = __buffer
                            expected_arg_count = ins["param_count"]
                        bytecode.append(ins["opcode"])
                    except KeyError:
                            print(__buffer, "not implemented. Is it even an instruction?")
                            exit(0)
                elif line[i] == "@":
                    __buffer += line[i]
                    i += 1
                    if i < len(line):
                        if not line[i].isspace():
                            while (i < len(line)) and line[i].isalpha():
                                __buffer += line[i]
                                i += 1
                        args_found += 1
                        bytecode.append(__buffer)

                        if expected_arg_count == args_found:
                            expecting_arg = False
                            expected_arg_count = args_found = 0
                            expecting_arg_for = ""

                else:
                    i += 1
                __buffer = ""
            if expecting_arg:
                print("Did not find all the arguments for", expecting_arg_for, ".line:",line_number)
                exit(0)

        for i,j in enumerate(bytecode):
            if isinstance(j, str):
                try:
                    bytecode[i] = jump_table[j[1:]]
                except KeyError:
                    print("Could not find declaration of", j[1:])
                    exit(0)
        #print(bytecode)
        return bytecode

