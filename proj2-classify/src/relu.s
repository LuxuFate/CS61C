.globl relu

.text
# ==============================================================================
# FUNCTION: Performs an inplace element-wise ReLU on an array of ints
# Arguments:
# 	a0 (int*) is the pointer to the array
#	a1 (int)  is the # of elements in the array
# Returns:
#	None
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 115.
# ==============================================================================
relu:
    # Prologue
    addi sp, sp, -12
    sw s0 0(sp)
    sw s1 4(sp)
    sw ra 8(sp)
    
    mv s0 a0 
    mv s1 a1 

    addi t0 x0 1
    bge a1 t0 loop_start
    li a1 115
    j exit2

loop_start:
    lw t1 0(s0)
    bge t1 t0 loop_continue
    sw x0 0(s0)

loop_continue:
	addi s0 s0 4
	addi s1 s1 -1

	beq s1 x0 loop_end
	j loop_start

loop_end:
    # Epilogue
    lw s0 0(sp)
    lw s1 4(sp)
    lw ra 8(sp)
    addi sp, sp, 12
    
	ret
