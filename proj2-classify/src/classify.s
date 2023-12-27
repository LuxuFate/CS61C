.globl classify

.text
classify:
    # =====================================
    # COMMAND LINE ARGUMENTS
    # =====================================
    # Args:
    #   a0 (int)    argc
    #   a1 (char**) argv
    #   a2 (int)    print_classification, if this is zero, 
    #               you should print the classification. Otherwise,
    #               this function should not print ANYTHING.
    # Returns:
    #   a0 (int)    Classification
    # Exceptions:
    # - If there are an incorrect number of command line args,
    #   this function terminates the program with exit code 121.
    # - If malloc fails, this function terminates the program with exit code 116 (though we will also accept exit code 122).
    #
    # Usage:
    #   main.s <M0_PATH> <M1_PATH> <INPUT_PATH> <OUTPUT_PATH>
    addi sp, sp, -52
    sw s0 0(sp)
    sw s1 4(sp)
    sw s2 8(sp)
    sw s3 12(sp)
    sw s4 16(sp)
    sw s5 20(sp)
    sw s6 24(sp)
    sw s7 28(sp)
    sw s8 32(sp)
    sw s9 36(sp)
    sw s10 40(sp)
    sw s11 44(sp)
    sw ra 48(sp)

    mv s1 a1 #argv pointer
    mv s2 a2 #print

    addi t0 x0 5
    bne a0 t0 error1

	# =====================================
    # LOAD MATRICES
    # =====================================

    # Load pretrained m0

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s3 a0

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s4 a0

    mv a1 s3
    mv a2 s4

    lw a0 4(s1)
    
    jal ra read_matrix

    mv s5 a0 #m0 pointer
    lw s6 0(s3) #m0 rows
    mv a0 s3
    jal ra free
    lw s7 0(s4) #m0 columns
    mv a0 s4
    jal ra free

    # Load pretrained m1

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s3 a0

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s4 a0

    mv a1 s3
    mv a2 s4
    lw a0 8(s1)
    
    jal ra read_matrix

    mv s8 a0 #m1 pointer
    lw s9 0(s3) #m1 rows
    mv a0 s3
    jal ra free
    lw s10 0(s4) #m1 columns
    mv a0 s4
    jal ra free

    # Load input matrix

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s3 a0

    addi a0 x0 4
    jal ra malloc
    beq a0 x0 error2
    mv s4 a0

    mv a1 s3
    mv a2 s4
    lw a0 12(s1)

    jal ra read_matrix

    mv s11 a0 #input pointer
    lw s0 0(s3) #input rows
    mv a0 s3
    jal ra free
    lw s3 0(s4) #input columns
    mv a0 s4
    jal ra free


    # =====================================
    # RUN LAYERS
    # =====================================
    # 1. LINEAR LAYER:    m0 * input
    # 2. NONLINEAR LAYER: ReLU(m0 * input)
    # 3. LINEAR LAYER:    m1 * ReLU(m0 * input)

    mul a0 s6 s3
    slli a0 a0 2
    jal ra malloc
    beq a0 x0 error2
    mv s4 a0

    mv a6 s4
    mv a0 s5
    mv a1 s6
    mv a2 s7
    mv a3 s11
    mv a4 s0
    mv a5 s3
    jal ra matmul

    mv a0 s5
    jal ra free

    mv s5 s4 #hidden layer (dont need m0 s5, s6, s7)

    mv a0 s5
    mul a1 s6 s3
    jal ra relu

    mv s5 a0 #relu(hidden layer)

    mul a0 s9 s3
    slli a0 a0 2
    jal ra malloc
    beq a0 x0 error2
    mv s7 a0

    mv a6 s7
    mv a0 s8
    mv a1 s9
    mv a2 s10
    mv a3 s5
    mv a4 s6
    mv a5 s3
    jal ra matmul

    mv s5 s7 #scores

    # =====================================
    # WRITE OUTPUT
    # =====================================
    # Write output matrix

    lw a0 16(s1)
    mv a1 s5
    mv a2 s9
    mv a3 s3
    jal ra write_matrix

    mv a0 s5
    jal ra free
    mv a0 s4
    jal ra free

    # =====================================
    # CALCULATE CLASSIFICATION/LABEL
    # =====================================
    # Call argmax

    mv a0 s5
    mul a1 s9 s3
    jal ra argmax

    # Print classification
    bne s2 x0 end
    mv a1 a0
    jal ra print_int

    # Print newline afterwards for clarity
end: 
    li a1 '\n'
    jal ra print_char

    mv a0 s8
    jal ra free
    mv a0 s11
    jal ra free

    #jal ra print_num_alloc_blocks

    lw s0 0(sp)
    lw s1 4(sp)
    lw s2 8(sp)
    lw s3 12(sp)
    lw s4 16(sp)
    lw s5 20(sp)
    lw s6 24(sp)
    lw s7 28(sp)
    lw s8 32(sp)
    lw s9 36(sp)
    lw s10 40(sp)
    lw s11 44(sp)
    lw ra 48(sp)
    addi sp, sp, 52

    ret

error1:
    li a1 121
    j exit2
    
error2:
    li a1 122
    j exit2
