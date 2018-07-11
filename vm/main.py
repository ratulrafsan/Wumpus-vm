from vm.CPU import CPU
from vm.assembler import assembler
import time

'''

### arithmetic test
((5+5)-2)^2
push 5
push 5
add
push 2
swap
sub
dup
mul
halt

##### jump test
push 5 //2
push 5 //4
add    //5
jmp    //6
push 6 //8
sub   //9
hlt   //10
push 1 //12
push 10 //14
sub //15
hlt //16
result should be 9


    00 nop
    01 add
    02 sub
    03 mul
    04 div
    05 mod
    06 dup
    07 push arg
    08 pop
    09 swap
    10 jmptos
    11 jmp addr
    12 halt
'''
                # 0  1  2  3  4   5  6  7  8  9  10  11  12  13  14  15  16  17, 18, 19, 20
import time
cpu = CPU(memory_size=1024)

asm = assembler()
program = asm.assemble(
    [line.replace(',', ' ').strip() for line in open("popprevTest.wasm","r")]
)
cpu.load_program(program)
start_time = time.clock()
cpu.execute()
print("Execution of fib(40) on wumpus took", time.clock()-start_time, "sec")


def fib(n):
    if n <= 0:
        return 1
    return n * fib(n-1)

start_time = time.clock()
res = fib(40)
print("Pure :", res, "\nExecution fib(40) in pure python took", time.clock() - start_time)



#