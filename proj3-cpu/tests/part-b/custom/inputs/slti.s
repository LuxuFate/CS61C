addi t0 x0 1
slti s0 t0 2
addi t0 x0 2
slti s1 t0 1

addi t1 x0 -2048
slti s1 t1 31

addi t1 x0 2047
slti s1 t1 31

addi t1 x0 -2048
slti s1 t1 0

addi t1 x0 2047
slti s1 t1 0