addi sp sp -100
addi s0 x0 23
sw s0 0(sp)
sw s0 4(sp)
lw s0 0(sp)
lw s0 4(sp)
addi t1 x0 2047
sw t1 0(sp)
sw t1 4(sp)
sw t1 8(sp)
lw t1 0(sp)
lw t1 4(sp)
lw t1 8(sp)
addi t1 x0 -2048
sw t1 0(sp)
sw t1 4(sp)
sw t1 8(sp)
lw t1 0(sp)
lw t1 4(sp)
lw t1 8(sp)