addi t0 x0 5
addi t1 x0 5
beq t0 t1 branch1

branch1:
	beq t0 t1 branch2
branch2:
	beq t0 t1 branch3
branch3:
	beq t0 t1 branch4
branch4:
	beq t0 t1 branch5

branch5:
	addi t0 t0 1
	bne t0 t1 branch6
branch6:
	bne t0 t1 branch7
branch7:
	bne t0 t1 branch8
branch8:
	bne t0 t1 branch9

branch9:
	bge t0 t1 branch10
branch10:
	bge t0 t1 branch11
branch11:
	bge t0 t1 branch12
branch12:
	bge t0 t1 branch13

branch13:
	addi t1 t1 10
	blt t0 t1 branch14
branch14:
	blt t0 t1 branch15
branch15:
	blt t0 t1 branch16
branch16:
	addi s1 x0 5
	addi s0 x0 0
	blt t0 t1 loop

loop:
	bgeu s0 s1 end
	addi s0 s0 1
	jal loop


end:
	addi s1 x0 4

