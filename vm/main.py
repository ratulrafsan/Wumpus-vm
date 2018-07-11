from vm.CPU import CPU
from vm.assembler import assembler

fileName = "tests/test3.wasm"

cpu = CPU(memory_size=1024)
asm = assembler()
program = asm.assemble(
    [line.replace(',', ' ').strip() for line in open(fileName, "r")]
)
cpu.load_program(program)
cpu.execute()