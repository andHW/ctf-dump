EXIT_0_ASM = """MOV R8, 2
MOV R1, 0
SYSCALL"""

# TODO: find this yourself: https://hackmd.io/@blackb6a/bauhinia-isa
FILE_READING_ASM = """NOP
NOP
NOP"""

asm_lines = FILE_READING_ASM.split("\n")

# prepend "JMP" to each line
for i in range(len(asm_lines)):
    asm_lines[i] = "JMP " + asm_lines[i]

magic1 = len("JMP 0x000000 JMP ")
begin = 0x400000

cur = begin + magic1

print(f"JMP {hex(cur)}", end="")

for line in asm_lines:
    print()
    print(line)
    l = len(line) - len("JMP ")
    cur = cur + l + 1 + magic1
    print(f"JMP {hex(cur)}", end="")
