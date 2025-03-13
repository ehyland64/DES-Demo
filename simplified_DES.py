def initial_permutation(sequence):
    return [sequence[i] for i in (1,5,2,0,3,7,4,6)]

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

def S_box_0(sequence):
    s_box_0_matrix = [[1, 0, 3, 2],
                      [2, 3, 1, 0],
                      [0, 2, 1, 3],
                      [3, 1, 3, 2]]
    
    # needs to extract first and last bits and then middle two bits individually
    first_and_last = int(sequence[0] + sequence[-1])
    middle = sequence[1] + sequence[2]
    
    # now, convert these two 2-bit sequences to digits so we may index the matrix to extract results.
    print(type(first_and_last))

    temp = 

   # print(s_box_0_matrix[first_last_int][middle_int])

    # we should return the 4 bit result derived from taking the matrix results:

    


def S_box_1(sequence):
    s_box_1_matrix = [[0, 1, 2, 3],
                      [2, 0, 1, 3],
                      [3, 0, 1, 0],
                      [2, 1, 0, 3]]



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
    number_of_subkeys = len(subkeys)
    rounds_completed = 0
    for i in range (0, len(subkeys)):
        print("Subkey " + str(i) + ": " + subkeys[i])
    
    
    # typically 16 rounds of Feistel cipher in DES
    while rounds_completed != number_of_feistel_rounds:
        # halve the message block
        left, right = message_block[:len(message_block) // 2], message_block[:len(message_block) // 2:]

        # pass right half to the expansion function
        expanded_right = expansion(right)
        current_subkey = subkeys[rounds_completed]
        print("current subkey test: " + current_subkey)

        print("expansion: " + expanded_right)
        print("current subkey: " + current_subkey)

        # the current subkey must be XOR with the expansion result
        xor_result = int(expanded_right) ^ int(current_subkey)
        xor_result = format(xor_result, 'b')
        print("XOR Result: " + xor_result)
        rounds_completed = 16

        # now we may halve the XOR result
        # XOR_left, XOR_right = temp[:len(temp) // 2], temp[len(temp) // 2:]

        # after, apply the permutatuon function the message block result



def DES_encrypt(message_block, master_key):
    subkeys = schedule_keys(master_key, 2)
    ciphertext = feistel_network(message_block, subkeys)
    return ciphertext



if __name__ == "__main__":
    message = '011101011'
    master_key = '0001010100'
    #ciphertext = DES_encrypt(message, master_key)
    # subkeys = schedule_keys(master_key, 2)
    # feistel_network(message, subkeys)
    S_box_0('0110')
   