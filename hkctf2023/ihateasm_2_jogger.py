exit_asm = """MOV R8, 2
MOV R1, 0
SYSCALL"""

asm = """MOV R8, 0
MOV R1, 0x410000
MOV R2, 100
SYSCALL
MOV R8, 3
MOV R1, 0x410000
MOV R2, 0x420000
MOV R3, 100
SYSCALL
MOV R2, R8
MOV R8, 1
MOV R1, 0x420000
SYSCALL
MOV R8, 2
MOV R1, 0
SYSCALL"""

asm = exit_asm

asm_lines = asm.split('\n')



# print('\n'.join(asm_lines))