.globl write_matrix

.text
# ==============================================================================
# FUNCTION: Writes a matrix of integers into a binary file
# FILE FORMAT:
#   The first 8 bytes of the file will be two 4 byte ints representing the
#   numbers of rows and columns respectively. Every 4 bytes thereafter is an
#   element of the matrix in row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is the pointer to the start of the matrix in memory
#   a2 (int)   is the number of rows in the matrix
#   a3 (int)   is the number of columns in the matrix
# Returns:
#   None
# Exceptions:
# - If you receive an fopen error or eof,
#   this function terminates the program with error code 112.
# - If you receive an fwrite error or eof,
#   this function terminates the program with error code 113.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 114.
# ==============================================================================
write_matrix:

    # Prologue
    addi sp, sp, -28
	sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    sw ra 24(sp)

    mv s0 a0 #filename string
    mv s1 a1 #matrix pointer
    mv s2 a2 #rows
    mv s3 a3 #columns

    mv a1 s0
    addi a2 x0 1
    jal ra fopen
    addi t0 x0 -1
    beq a0 t0 error1

    mv s4 a0 #file descriptor


    mv a1 s4

    addi sp sp -4
    sw s2 0(sp)
    mv a2 sp #pointer
    addi sp sp 4

    addi t0 x0 1
    mv a3 t0
    addi t0 x0 4
    mv a4 t0
    jal ra fwrite
    addi t0 x0 1
    bne a0 t0 error2


    mv a1 s4

    addi sp sp -4
    sw s3 0(sp)
    mv a2 sp #pointer
    addi sp sp 4

    addi t0 x0 1
    mv a3 t0
    addi t0 x0 4
    mv a4 t0
    jal ra fwrite
    addi t0 x0 1
    bne a0 t0 error2

    addi s5 x0 0
    mul s5 s2 s3 #number of elements

    mv a1 s4
    mv a2 s1
    mv a3 s5
    addi a4 x0 4
    jal ra fwrite
    bne a0 s5 error2

    mv a1 s4
    jal ra fclose
    bne a0 x0 error3

    # Epilogue
    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw ra 24(sp)
    addi sp, sp, 28

    ret

error1:
    li a1 112
    j exit2
    
error2:
    li a1 113
    j exit2

error3:
    li a1 114
    j exit2
