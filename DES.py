def initial_permutation(sequence):
    return "".join([sequence[i] for i in (1,5,2,0,3,7,4,6)])

# P10 = (2, 4, 1, 6, 3, 9, 0, 8, 7, 5)
def P10(sequence):
    return "".join([sequence[i] for i in (2, 4, 1, 6, 3, 9, 0, 8, 7, 5)])


# P8 = (5,2,6,3,7,4,9,8)
def P8(sequence):
    return "".join([sequence[i] for i in (5, 2, 6, 3, 7, 4, 9, 8)])


# P4 = (1, 3, 2, 0)
def P4(sequence):
    return "".join([sequence[i] for i in (1, 3, 2, 0)])


# now we need to define the permutation applied to the result of a Feistel network
def permutation_O(sequence):
    return "".join([sequence[i] for i in (4, 5, 6, 7, 0, 1, 2, 3)])


# this is a customisable expansion function for use within a Feistel network. Expands block of 4-bit to 8-bit.
def expansion(sequence):
    return "".join([sequence[i] for i in (3, 0, 1, 2, 1, 2, 3, 0)])


# define some S-Boxes.

def S_box(left_sequence, right_sequence):
    s_box_0_matrix = [[1, 0, 3, 2],
                      [2, 3, 1, 0],
                      [0, 2, 1, 3],
                      [3, 1, 3, 2]]
    
    s_box_1_matrix = [[0, 1, 2, 3],
                      [2, 0, 1, 3],
                      [3, 0, 1, 0],
                      [2, 1, 0, 3]]
    
    # needs to extract first and last bits and then middle two bits individually within each s-box
    first_and_last_s0_box, first_and_last_s1_box = int(left_sequence[0] + left_sequence[-1], 2), int(right_sequence[0] + right_sequence[-1], 2)
    middle_s0_box, middle_s1_box = int(left_sequence[1] + left_sequence[-1], 2), int(right_sequence[1] + right_sequence[-1], 2)
    s0_result, s1_result = format(s_box_0_matrix[first_and_last_s0_box][middle_s0_box], 'b'), format(s_box_1_matrix[first_and_last_s1_box][middle_s1_box], 'b')
    # we will need to add enough 0s to tbe beginning of this result to ensure our output is 4-bits length.
    final_result = s0_result + s1_result
    if len(final_result) < 4:
        zeros_needed = "0" * (4 - len(final_result))
        final_result = zeros_needed + final_result

    # return the 4-bit result
    return final_result


# define a key scheduler
def schedule_keys(master_key, number_of_subkeys):
    subkeys = [0] * number_of_subkeys
    subkey_count = 1
    keys_needed = True
    P10_result = P10(master_key)


    while keys_needed:
        left, right = P10_result[:len(P10_result) // 2], P10_result[len(P10_result) // 2:]

        # determine correct number of cyclic shifts needed
        shifts_needed = 1 if subkey_count in [1, 2, 9, 16] else 2

        # shift the left and right halves of the P10 result.
        # this takes the last elements and adds the first elements in the key up until the amount of shifts needed.
        left = left[shifts_needed:] + left[:shifts_needed]
        right = right[shifts_needed:] + right[:shifts_needed]

        # add these segments back together to return an 8-bit key and generate the subkey
        subkey = P8(left + right)
        subkeys[subkey_count - 1] = subkey

        # check if any more keys need to be generated.
        if number_of_subkeys == subkey_count:
            keys_needed = False
        else:
            P10_result = left + right
            subkey_count += 1
    
    # keys generated, return subkeys for use in the Feistel network
    return subkeys


def feistel_network(message_block, subkeys, number_of_feistel_rounds=16):
    message_block = initial_permutation(message_block)
    rounds_completed = 0
    for i in range (0, len(subkeys)):
        print("Subkey " + str(i + 1) + ": " + subkeys[i])
    
    
    # typically 16 rounds of Feistel cipher in DES
    while rounds_completed != number_of_feistel_rounds:
        print("current round number: " + str(rounds_completed))
        
        # halve the message block
        left, right = message_block[:len(message_block) // 2], message_block[:len(message_block) // 2:]

        # pass right half to the expansion function
        print("message block length: " + str(len(message_block)))
        print("right length: " + str(len(right)))
        expanded_right = expansion(right)
        print("testing: " + subkeys[rounds_completed])
        current_subkey = (subkeys[rounds_completed])

        # the current subkey must be XOR with the expansion result
        xor_result = format((int(expanded_right, 2) ^ int(current_subkey, 2)), 'b')
        print("XOR = " + xor_result)

        # pass this result to the P4 function
        P4_result = P4(xor_result)
        print("left hand side message block length (should be 4): " + str(len(left)))

        # now, XOR this P4 result with the original left half of the message block.
        # left and right are lists, but shouldn't be
        P4_and_original_left_message_xor = format((int(left, 2) ^ int(P4_result, 2)), 'b')

        # need to also ensure that this has any leading 0s that may be left out of the XOR operation
        if len(P4_and_original_left_message_xor) < 4:
            zeros_needed = "0" * (4 - len(P4_and_original_left_message_xor))
            P4_and_original_left_message_xor = zeros_needed + P4_and_original_left_message_xor


        print("p4 length before xor: " + str(len(P4_result)))
        print("p4 XOR length: " + str(len(P4_and_original_left_message_xor)))

        # finally, we can combine this result with the original right hand side of the message block with this final XOR result.
        
        # this final result will either be input to the following Feistle network or it will represent the final ciphertext.
        final_permutation = P4_and_original_left_message_xor + right
        message_block = final_permutation
        rounds_completed += 1
    
    # return the final ciphertext
    return message_block
        





def DES_encrypt(message_block, master_key):
    subkeys = schedule_keys(master_key, 2)
    ciphertext = feistel_network(message_block, subkeys)
    return ciphertext



if __name__ == "__main__":
    message = '00010111'
    master_key = '0001010100'
    #ciphertext = DES_encrypt(message, master_key)
    subkeys = schedule_keys(master_key, 16)
    feistel_network(message, subkeys)
   