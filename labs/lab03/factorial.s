.globl factorial

.data
n: .word 8

.text
main:
    la t0, n
    lw a0, 0(t0)
    jal ra, factorial

    addi a1, a0, 0
    addi a0, x0, 1
    ecall # Print Result

    addi a1, x0, '\n'
    addi a0, x0, 11
    ecall # Print newline

    addi a0, x0, 10
    ecall # Exit

factorial:
    addi a2, x0, 0
    add a3, x0, a0
    
loop:
	addi a2, a2, 1
    beq a2, a3, exit
    sub a4, a3, a2
    mul a0, a0, a4
    jal x0, loop
    
exit:
    jr ra
    