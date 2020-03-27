"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4  # set the last reg to the sp
        self.pc = 0
        self.fl = 0

    # op codes and handler
        self.handler = {
            0b10100000: self.handle_ADD,
            0b10101000: self.handle_AND,
            0b01010000: self.handle_CALL,
            0b10100111: self.handle_CMP,
            0b00000001: self.handle_HLT,
            0b01010101: self.handle_JEQ,
            0b01011010: self.handle_JGE,
            0b01010111: self.handle_JGT,
            0b01011001: self.handle_JLE,
            0b01011000: self.handle_JLT,
            0b01010100: self.handle_JMP,
            0b01010110: self.handle_JNE,
            0b10000010: self.handle_LDI,
            0b10100100: self.handle_MOD,
            0b10100010: self.handle_MUL,
            0b01101001: self.handle_NOT,
            0b10101010: self.handle_OR,
            0b01000110: self.handle_POP,
            0b01000111: self.handle_PRN,
            0b01000101: self.handle_PUSH,
            0b00010001: self.handle_RET,
            0b10101100: self.handle_SHL,
            0b10101101: self.handle_SHR,
            0b10101011: self.handle_XOR,

        }

    def load(self, file):
        """Load a program into memory."""

        address = 0

        with open(file) as f:
            lines = f.readlines()
            lines = [
                line for line in lines if line.startswith('0') or line.startswith('1')
            ]
            program = [int(line[:8], 2) for line in lines]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def handle_instructions(self, op, reg_a, reg_b):
        """CU operations."""
        try:
            self.handler[op](reg_a, reg_b)
        except KeyError:
            raise Exception("No such op code")

    def handle_ADD(self, reg_a, reg_b):
         self.reg[reg_a] += self.reg[reg_b]
         self.pc += 3

    def handle_AND(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        self.pc += 3

    
    def handle_CALL(self, reg_a, reg_b):
       self.reg[7] -= 1
       self.ram_write(self.pc + 2, self.reg[7])
       self.pc = self.reg[reg_a]

    def handle_CMP(self, reg_a, reg_b):
        self.fl = 0b00000000
        if self.reg[reg_a] == self.reg[reg_b]:
            self.fl = 0b00000001
        if self.reg[reg_a] < self.reg[reg_b]:
            self.fl = 0b00000100
        if self.reg[reg_a] > self.reg[reg_b]:
            self.fl = 0b00000010
        self.pc += 3
        
        
    def handle_HLT(self, reg_a, reg_b):
        self.pc += 1
        self.running = False

    def handle_JEQ(self, reg_a, reg_b):
        if self.fl == 0b00000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        

    def handle_JGE(self, reg_a, reg_b):
        if self.fl == 0b00000001 or self.fl == 0b00000010:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        

    def handle_JGT(self, reg_a, reg_b):
        if self.fl == 0b00000010:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        
    
    def handle_JLE(self, reg_a, reg_b):
        if self.fl == 0b00000100 or self.fl == 0b00000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        
    def handle_JLT(self, reg_a, reg_b):
        if self.fl == 0b00000100:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        

    def handle_JMP(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]

    def handle_JNE(self, reg_a, reg_b):
        if self.fl != 0b0000001:
            self.pc = self.reg[reg_a]
        else:
            self.pc += 2
        
    def handle_LDI(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b
        self.pc += 3

    def handle_MOD(self, reg_a, reg_b):
        if self.reg[reg_b] == 0:
            return
        self.reg[reg_a] = (self.reg[reg_a] % self.reg[reg_b])
        self.pc += 3  
    
    def handle_MUL(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] * self.reg[reg_b])
        self.pc += 3

    def handle_NOT(self, reg_a, reg_b):
        self.reg[reg_a] = ~self.reg[reg_a]
        self.pc += 2

    def handle_OR(self, reg_a, reg_b):
        self.reg[reg_a] = (self.reg[reg_a] | self.reg[reg_b])
        self.pc += 3   

    def handle_POP(self, reg_a, reg_b):
        self.reg[reg_a] = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.pc += 2
        return self.reg[reg_a]

    def handle_PRN(self, reg_a, reg_b):
        print(self.reg[reg_a])
        self.pc += 2

    def handle_PUSH(self, reg_a, reg_b):
        self.reg[7] -= 1
        self.ram_write(self.reg[reg_a], self.reg[7])
        self.pc += 2

    def handle_RET(self, reg_a, reg_b):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def handle_SHL(self, reg_a, reg_b):
        self.reg[reg_a] << self.reg[reg_b]
        self.pc += 3   

    def handle_SHR(self, reg_a, reg_b):
        self.reg[reg_a] >> self.reg[reg_b]
        self.pc += 3   

    def handle_XOR(self, reg_a, reg_b):
        self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        self.pc += 3   

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        # set exit condition
        self.running = True

        # while loop
        while self.running:

            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            self.handle_instructions(IR, operand_a, operand_b)
