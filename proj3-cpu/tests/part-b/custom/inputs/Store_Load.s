addi a0 a0 -100
addi s0 x0 4
addi s1 x0 5
addi t0 x0 6
addi t1 x0 7

sw s0 0(a0)
sw s1 4(a0)
sw t0 8(a0)
sw t1 12(a0)

lw s0 0(a0)
lw s1 4(a0)
lw t0 8(a0)
lw t1 12(a0)

sh s0 0(a0)
sh s0 1(a0)
sh s1 2(a0)
sh t0 4(a0)
sh t1 5(a0)

lh s0 0(a0)
lh s0 1(a0)
lh s1 2(a0)
lh t0 4(a0)
lh t1 22(a0)

addi s0 x0 1234
addi s1 x0 123
addi t0 x0 321
addi t1 x0 2047

sw s0 0(a0)
sw s1 -4(a0)
sw t0 -8(a0)
sw t1 -12(a0)

lw s0 0(a0)
lw s1 -4(a0)
lw t0 -8(a0)
lw t1 -12(a0)

sh s0 0(a0)
sh s0 -3(a0)
sh s1 -2(a0)
sh t0 -4(a0)

lh s0 0(a0)
lh s0 -3(a0)
lh s1 -2(a0)
lh t0 -4(a0)
