jal x0 jump
jump:
	jal ra jump2
addi t0 x0 2047
addi t1 x0 2047
jump2:
	jal x0 jump3
jump3:
	jal x0 jump4
jump4:
	jal x0 jump5
jump5:
	jal ra jump10
addi t0 x0 2047
addi t1 x0 2047
jump6:
	jal x0 jump9
jump7:
	jal x0 jump8
jump8:
	jal x0 end
jump9:
	jal x0 jump7
jump10:
	jal x0 jump6
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
add x0 x0 x0
end:
	addi t0 t0 1
