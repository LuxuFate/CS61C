.globl read_matrix

.text
# ==============================================================================
# FUNCTION: Allocates memory and reads in a binary file as a matrix of integers
#
# FILE FORMAT:
#   The first 8 bytes are two 4 byte ints representing the # of rows and columns
#   in the matrix. Every 4 bytes afterwards is an element of the matrix in
#   row-major order.
# Arguments:
#   a0 (char*) is the pointer to string representing the filename
#   a1 (int*)  is a pointer to an integer, we will set it to the number of rows
#   a2 (int*)  is a pointer to an integer, we will set it to the number of columns
# Returns:
#   a0 (int*)  is the pointer to the matrix in memory
# Exceptions:
# - If malloc returns an error,
#   this function terminates the program with error code 116.
# - If you receive an fopen error or eof, 
#   this function terminates the program with error code 117.
# - If you receive an fread error or eof,
#   this function terminates the program with error code 118.
# - If you receive an fclose error or eof,
#   this function terminates the program with error code 119.
# ==============================================================================
read_matrix:

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

    mv s0 a0 #filename string
    mv s1 a1 #row pointer
    mv s2 a2 #column pointer

    #lw a1 0(a0)
    #jal ra print_str

    mv a1 s0
    addi a2 x0 0
    jal ra fopen
    addi t0 x0 -1
    beq a0 t0 error2

    mv t0 x0

    mv s3 a0 #file descriptor

    #Reading the row
    mv a1 s3
    mv a2 s1 #row
    addi t0 x0 4
    mv a3 t0

    addi sp sp -4
    sw t0 0(sp)
    jal ra fread
    lw t0 0(sp)
    addi sp sp 4

    bne a0 t0 error3

    lw s4 0(s1) #number of rows

    #Reading the Column
    mv a1 s3
    mv a2 s2 #column
    mv a3 t0

    addi sp sp -4
    sw t0 0(sp)
    jal ra fread
    lw t0 0(sp)
    addi sp sp 4

    bne a0 t0 error3

    lw s5 0(s2) #number of columns


    addi s6 x0 0
    mul s6 s4 s5
    slli s6 s6 2 #number of bytes
    mv a0 s6
    jal ra malloc
    beq a0 x0 error1

    addi s7 x0 0
    mv s7 a0

    mv a1 s3
    mv a2 s7
    mv a3 s6
    jal ra fread
    bne a0 s6 error3

    mv a1 s3
    jal ra fclose
    bne a0 x0 error4

    mv a0 s7
    mv a1 s1
    mv a2 s2

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
    li a1 116
    j exit2
    
error2:
    li a1 117
    j exit2

error3:
    li a1 118
    j exit2

error4:
    li a1 119
    j exit2
