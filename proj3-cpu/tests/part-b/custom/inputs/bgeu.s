addi t0 x0 -7
addi t1 x0 4
bgeu t0 t1 label
addi t0 x0 45
label:
	addi t0 x0 1
	bgeu t0 t1 label
	addi t0 x0 4
	bgeu t0 t1 label2

label2:
	addi t0 x0 -9
	addi t1 x0 9
	bgeu t0 t1 done
	

done:
	addi t0 x1 33