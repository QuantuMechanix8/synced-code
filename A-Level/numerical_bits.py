from functools import reduce
import operator
def half_adder(first_bit, second_bit):
    bit1, bit2 = bool(int(first_bit)), bool(int(second_bit))
    sum = (bit1 or bit2) and not (bit1 and bit2) # xor the two bits give sum bit
    carry = bit1 and bit2
    
    sum_bit, carry_bit = str(int(sum)), str(int(carry))
    return (sum_bit, carry_bit)


def full_adder(first_bit, second_bit, carry_bit):
    bits_sum, bits_carry = half_adder(first_bit, second_bit)
    sum, other_carry = half_adder(bits_sum, carry_bit)
    carry = half_adder(bits_carry, other_carry)[0]
    
    return (sum, carry)

def add(bin_num_str1, bin_num_str2, carry = "0"):
    if len(bin_num_str1) == 0 and len(bin_num_str2) == 0 and carry == "0":
        return ""
    elif len(bin_num_str1) == 0 and len(bin_num_str2) == 0:
        return carry

    if len(bin_num_str1) == 0:
        bin_num_str1 = "0"
    elif len(bin_num_str2) == 0:
        bin_num_str2 = "0"

    end_bit1, end_bit2 = bin_num_str1[-1], bin_num_str2[-1]
    sum, carry = full_adder(end_bit1, end_bit2, carry)
    return add(bin_num_str1[:-1], bin_num_str2[:-1], carry) + sum
    
def twos_compliment(bin_num_str, to_negative=True):
    """converts a binary integer to its two's complement - will ensure the first bit is 1 if to_negative=True"""
    num_length = len(bin_num_str)
    if to_negative and bin_num_str[0] == "1":
        bin_num_str = "0" + bin_num_str

    flipped_bin_num_str = reduce(operator.add, ["0" if char == "1" else "1" for char in bin_num_str])
    print(flipped_bin_num_str)
    return add(flipped_bin_num_str, "1")[-num_length:]
