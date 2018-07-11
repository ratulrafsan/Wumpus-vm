'''
each instruction has three attributes:
    op_code -> operation code
    param_count -> number of parameters taken from memory
    pop_count -> number of items popped form operation stack
'''

op_codes = {mnemonic: code for code, mnemonic in enumerate(["nop", "add", "sub", "push", "pop"])}


