.globl argmax

.text
# =================================================================
# FUNCTION: Given a int vector, return the index of the largest
#	element. If there are multiple, return the one
#	with the smallest index.
# Arguments:
# 	a0 (int*) is the pointer to the start of the vector
#	a1 (int)  is the # of elements in the vector
# Returns:
#	a0 (int)  is the first index of the largest element
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 120.
# =================================================================
argmax:
    # Prologue
    addi sp, sp, -12
    sw s0 0(sp)
    sw s1 4(sp)
    sw ra 8(sp)
    
    mv s0 a0
    mv s1 a1
    lw t2 0(s0) 
    addi t4 x0 0 #largest index
	addi t1 x0 0 #current index

    addi t0 x0 1
    bge a1 t0 loop_start
    li a1 120
    j exit2

loop_start:
	lw t3 0(s0)
    bge t2 t3 loop_continue
    mv t2 t3
	mv t4 t1
    
loop_continue:
	addi s0 s0 4
    addi s1 s1 -1
    addi t1 t1 1
    
    beq s1 x0 loop_end
	j loop_start

loop_end:
    # Epilogue
    lw s0 0(sp)
    lw s1 4(sp)
    lw ra 8(sp)
    addi sp, sp, 12
	mv a0 t4
    ret
