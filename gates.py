def AND(a , b):
    if a == 1 and b == 1:
        return 1
    else:
        return 0

def OR(a, b):
    if a == 1 or b == 1:
        return 1
    else:
        return 0

def NOT(a):
    if a != 1:
        return 1
    if a != 0:
        return 0 

def XOR(a, b):
    if a != b:
        return 1
    else:
        return 0

def HALF_ADDER(a, b):
    sum_result = XOR(a, b)
    carry_result = AND(a, b)
    return sum_result, carry_result

def FULL_ADDER(a, b, carry_in):
    sum1 , carry1 = HALF_ADDER(a, b)
    final_sum, carry2 = HALF_ADDER(sum1, carry_in)
    carry_out = OR(carry1, carry2)
    return final_sum, carry_out




def FOUR_BIT_ADDER(a0, a1, a2, a3, b0, b1, b2, b3, carry_in):
    sum0, carry0 = FULL_ADDER(a0, b0, carry_in)
    sum1, carry1 = FULL_ADDER(a1, b1, carry0)
    sum2, carry2 = FULL_ADDER(a2, b2, carry1)
    sum3, carry3 = FULL_ADDER(a3, b3, carry2)
    return sum3, sum2, sum1, sum0, carry3

def FOUR_BIT_SUBTRACTOR(a0, a1, a2, a3, b0, b1, b2, b3, carry_in):
    b0 = NOT(b0)
    b1 = NOT(b1)
    b2 = NOT(b2)
    b3 = NOT(b3)
    carry_in = 1
    sum3, sum2, sum1, sum0, carry3 = FOUR_BIT_ADDER(a0, a1, a2, a3, b0, b1, b2, b3, carry_in)
    return sum3, sum2, sum1, sum0, carry3

#print(FOUR_BIT_SUBTRACTOR(0, 1, 1, 0, 0, 1, 0, 0, 1))   #01001
#print(FOUR_BIT_ADDER(0, 1, 1, 0, 0, 1, 0, 0, 1))
# function for ALU selector 

def ALU_SELECTOR(selector, a0, a1, a2, a3, b0, b1, b2, b3, carry_in):
    if selector == 1:
        print(FOUR_BIT_ADDER(a0, a1, a2, a3, b0, b1, b2, b3, carry_in))
    elif selector == 0:
        print(FOUR_BIT_SUBTRACTOR(a0, a1, a2, a3, b0, b1, b2, b3, carry_in))
    else:
        print("ERROR")

#print(ALU_SELECTOR(1, 0, 1, 1, 0, 0, 1, 0, 0, 1))

def decimal_to_bits(value):
    a0 = value % 2
    value = value // 2
    a1 = value % 2
    value = value // 2
    a2 = value % 2
    value = value // 2
    a3 = value % 2
    return a0, a1, a2, a3


def binary_to_decimal(bit3, bit2, bit1, bit0):
    result = (bit3 * 8) + (bit2 * 4) + (bit1 * 2) + (bit0 * 1)
    return result

program = [ 
    "load R0, 5",
    "load R1, 2",
    "load R2, 4",
    "load R3, 1",
    "add R0, R1",
    "add R0, R2",
    "add R2, R3",
    "store M0, R0",
    "store M1, R2",
    "add R1, R3",
    "store M2, R1",
    "print M0",
    "print M1",
    "print M2"
]
registers = [0, 0, 0, 0]
memory = [0, 0, 0, 0]

for line in program:
    parts = line.split()
    parts[1] = parts[1].strip(",")
    #print(parts)
    
    if parts[0] == "load":
        reg_num = int(parts[1][1])
        value = int(parts[2])
        registers[reg_num] = value
        #print(registers)

    if parts[0] == "add":
        reg1 = int(parts[1][1])
        reg2 = int(parts[2][1])
        value1 = registers[reg1]
        value2 = registers[reg2] 
        a0, a1, a2, a3 = decimal_to_bits(value1)
        #print(a0, a1, a2, a3)
        b0, b1, b2, b3 = decimal_to_bits(value2)
        carry_in = 0
        sum3, sum2, sum1, sum0, carry3 = FOUR_BIT_ADDER(a0, a1, a2, a3, b0, b1, b2, b3, carry_in)
        final_sum = binary_to_decimal(sum3, sum2, sum1, sum0)
        #print(final_sum)
        registers[reg1] = final_sum
        #print(registers)
        
    #if for subtract??
    
    #if for print
    if parts[0] == "store":
        mem1 = int(parts[1][1])
        reg1 = int(parts[2][1])
        value = registers[reg1]
        memory[mem1] = value
        #print(memory)

    if parts[0] == "print":
        mem1 = int(parts[1][1])
        value = memory[mem1]
        print(value)
