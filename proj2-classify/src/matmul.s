.globl matmul

.text
# =======================================================
# FUNCTION: Matrix Multiplication of 2 integer matrices
# 	d = matmul(m0, m1)
# Arguments:
# 	a0 (int*)  is the pointer to the start of m0 
#	a1 (int)   is the # of rows (height) of m0
#	a2 (int)   is the # of columns (width) of m0
#	a3 (int*)  is the pointer to the start of m1
# 	a4 (int)   is the # of rows (height) of m1
#	a5 (int)   is the # of columns (width) of m1
#	a6 (int*)  is the pointer to the the start of d
# Returns:
#	None (void), sets d = matmul(m0, m1)
# Exceptions:
#   Make sure to check in top to bottom order!
#   - If the dimensions of m0 do not make sense,
#     this function terminates the program with exit code 125.
#   - If the dimensions of m1 do not make sense,
#     this function terminates the program with exit code 126.
#   - If the dimensions of m0 and m1 don't match,
#     this function terminates the program with exit code 127.
# =======================================================
matmul:
    # Error checks
    addi t0 x0 1
    blt a1 t0 error1
    blt a2 t0 error1
    blt a4 t0 error2
    blt a5 t0 error2
    bne a2 a4 error3

    # Prologue
    addi sp, sp, -36
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    sw s6 24(sp)
    sw s7 28(sp)
    sw ra 32(sp)

    mv s0 a0 #m0

    mv s1 a1 #m0 rows
    mv s2 a2 #m0 columns

    mv s3 a3 #m1

    mv s4 a4 #m1 rows
    mv s5 a5 #m1 columns

    mv s6 a6 #destination
    mv s7 a3 #original m1

    addi t1 x0 0 # m1 counter
    addi t2 x0 0 # m0 counter

outer_loop_start:

	addi t1 x0 0 #reset m1 counter
	mv s3 s7 # reset m1 pointer

inner_loop_start:
	mv a0 s0 #m0 row p
	mv a1 s3 #m1 col p
	mv a2 s2 #m0 col
	addi a3 x0 1 #1
	mv a4 s5 #ml col

	addi sp, sp, -24
    sw t0 0(sp)
    sw t1 4(sp)
    sw t2 8(sp)
    sw t3 12(sp)
    sw t4 16(sp)
    sw ra 20(sp)

	jal ra dot

	lw t0 0(sp)
    lw t1 4(sp)
    lw t2 8(sp)
    lw t3 12(sp)
    lw t4 16(sp)
    lw ra 20(sp)
    addi sp, sp, 24

	sw a0 0(s6)
	addi s6 s6 4

	addi s3 s3 4 # next col of m1
	addi t1 t1 1

	bne t1 s5 inner_loop_start
	j inner_loop_end

inner_loop_end:
	slli t3 s2 2
	add s0 s0 t3 #next row of m0
	addi t2 t2 1

	bne t2 s1 outer_loop_start
	j outer_loop_end


outer_loop_end:
    # Epilogue
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw s6 24(sp)
    lw s7 28(sp)
    lw ra 32(sp)
    addi sp, sp, 36
    
    ret


error1:
    li a1 125
    j exit2
    
error2:
    li a1 126
    j exit2

error3:
    li a1 127
    j exit2
