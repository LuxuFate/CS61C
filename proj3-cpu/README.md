# CS61CPU

I made a CPU! Here's what I did:

Part A:
	ALU: I had one MUX to select which operation my ALU did, which had 16 different inputs from the various instructions. Each one took input a and b, and output the result to the MUX.

	RegFile: I first figured out the 9 registers that were exposed. To tell which register to write to, I used a DeMUX, which used the write_reg and write_en as input. This allows me to select which register to write to if write_en is on. Each register had a write_data as input, output from the DeMUX to tell if they were enabled or not, and the clock. For read_data, I used a MUX which looked at rs1 and rs2 and outputed the corresponding register to read_data1 and read_data2.


	addi: I hardcoded for just the addi instruction to finish part a. For imm-gen, I just took the instruction and took the bits of the immediate from it and outputted the 32 bit extended one. For cpu, I took the instruction and split it into its respective parts for the I instructions. Inputted the instruction into the imm-gen to get the value of the immediate. Then I just inputted everything int my regfile and ALU to: get the value of the register, compute the value after adding, and write back to the register. 

Part B:

	In my control logic, I tried to find which instruction it was first my breaking down the instruction into its opcode, funct3, and funct7. And then I used those to create all of the control logic by mainly using muxes, gates, splitters, and priority encoders. This will tell my cpu which signals are on or off or otherwise. And then my cpu follows the risc-v datapath closely. I used a lot of tunnels so there are not a lot of wires everywhere. The worst bug I encountered was the situation with load and store. Where I have to make the write_enable mask myself, as well as make sure the loads are of the right size and of the right offset using splitters and shifters. 
