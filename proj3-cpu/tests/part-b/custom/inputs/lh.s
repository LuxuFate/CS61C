addi sp sp -100
addi s1 x0 23
sh s1 0(sp)
sh s1 1(sp)
sh s1 2(sp)

lh s1 0(sp)
lh s1 1(sp)
lh s1 2(sp)

addi t1 x0 2047
sh t1 4(sp)
sh t1 5(sp)
sh t1 6(sp)

lh t1 4(sp)
lh t1 5(sp)
lh t1 6(sp)

addi t1 x0 -2048
sh t1 8(sp)
sh t1 9(sp)
sh t1 10(sp)

lh t1 8(sp)
lh t1 9(sp)
lh t1 10(sp)