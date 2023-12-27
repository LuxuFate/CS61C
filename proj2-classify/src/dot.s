.globl dot

.text
# =======================================================
# FUNCTION: Dot product of 2 int vectors
# Arguments:
#   a0 (int*) is the pointer to the start of v0
#   a1 (int*) is the pointer to the start of v1
#   a2 (int)  is the length of the vectors
#   a3 (int)  is the stride of v0
#   a4 (int)  is the stride of v1
# Returns:
#   a0 (int)  is the dot product of v0 and v1
# Exceptions:
# - If the length of the vector is less than 1,
#   this function terminates the program with error code 123.
# - If the stride of either vector is less than 1,
#   this function terminates the program with error code 124.
# =======================================================
dot:
    # Prologue
    addi sp, sp, -24
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw ra 20(sp)

    mv s0 a0 #v0
    mv s1 a1 #v1
    mv s2 a2 #len
    slli s3 a3 2 #stride v0
    slli s4 a4 2 #stride v1

    addi t1 x0 0 # total

    addi t0 x0 1
    blt a2 t0 error1
    blt a3 t0 error2
    blt a4 t0 error2

loop_start:
	lw t2 0(s0)
	lw t3 0(s1)
	mul t4 t2 t3
	add t1 t1 t4

	add s0 s0 s3
	add s1 s1 s4
	addi s2 s2 -1

	bne s2 x0 loop_start


loop_end:
    # Epilogue
    
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw ra 20(sp)
    addi sp, sp, 24
    mv a0 t1
    
    ret

error1:
    li a1 123
    j exit2
    
error2:
    li a1 124
    j exit2
    
