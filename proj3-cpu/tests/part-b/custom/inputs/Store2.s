addi s0 x0 1234
addi s1 x0 123
addi t0 x0 321
addi t1 x0 2047

sb s0 120(sp)
sb s1 121(sp)
sb t0 122(sp)
sb t1 123(sp)
sb s1 124(sp)

lb s0 120(sp)
lb s1 121(sp)
lb t0 122(sp)
lb t1 123(sp)
lb s1 124(sp)

sb s0 -80(sp)
sb s1 -81(sp)
sb t0 -82(sp)
sb t1 -83(sp)
sb s1 -84(sp)

lb s0 -80(sp)
lb s1 -81(sp)
lb t0 -82(sp)
lb t1 -83(sp)
lb s1 -84(sp)