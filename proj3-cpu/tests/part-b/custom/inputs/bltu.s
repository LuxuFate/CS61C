addi t0 x0 3
addi t1 x0 -4
bltu t0 t1 label
addi t0 x0 45
label:
	addi t1 x0 -5
	bltu t0 t1 end

end:
	addi t0 x1 33
