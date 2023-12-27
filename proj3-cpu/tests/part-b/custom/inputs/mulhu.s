addi t0 x0 321
addi t1 x0 -321
mul s0 t0 t1
mulhu s0 s0 t0
addi t0 x0 444
addi t1 x0 444
mulhu s1 t0 t1

addi t0 x0 2047
mul s0 t0 t0
mul s0 s0 s0
mul s0 s0 s0
addi t0 x0 -2
mul s0 s0 t0
mulhu s1 s0 s0