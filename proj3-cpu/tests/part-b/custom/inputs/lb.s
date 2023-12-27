addi sp sp -100
addi s0 x0 23
sb s0 0(sp)
sb s0 1(sp)
sb s0 2(sp)
sb s0 3(sp)

lb s0 0(sp)
lb s0 1(sp)
lb s0 2(sp)
lb s0 3(sp)

addi t1 x0 2047
sb t1 4(sp)
sb t1 5(sp)
sb t1 6(sp)
sb t1 7(sp)

lb t1 4(sp)
lb t1 5(sp)
lb t1 6(sp)
lb t1 7(sp)

addi t1 x0 -2048
sb t1 8(sp)
sb t1 9(sp)
sb t1 10(sp)
sb t1 11(sp)

lb t1 8(sp)
lb t1 9(sp)
lb t1 10(sp)
lb t1 11(sp)