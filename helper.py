import pickle as pk
from qiskit import QuantumCircuit
import random as rd

from typing import overload

MESSAGE_BITS = (0, 1)
EMPTY= -1
POSSIBLE_BASES = ['H', 'D']

POSSIBLE_GATES = ['x', 'h', 'z', 'cx']

SMALL_KEY_LENGTH = 16
MAX_KEY_LENGTH = 48
SIMULATOR_METHOD = "matrix_product_state"

# random message
def generate_random_bits(length):
    bits = [rd.choice(MESSAGE_BITS) for _ in range(length)]
    return bits

def Generate_random_bases(key_length):
    hf_key = int(key_length / 2)
    bases = [POSSIBLE_BASES[0]] * hf_key + [POSSIBLE_BASES[1]] * (key_length - hf_key)
    # print(bases)

    rd.shuffle(bases)
    return bases

@overload
def encrypter_decrypter(A:str) -> list: ...
@overload
def encrypter_decrypter(A:list) -> str: ...

def encrypter_decrypter(A:str|list):
    if(isinstance(A, str)):
        ascii_value = ord(A)  # Get the ASCII value of the character
        binary_string = bin(ascii_value)[2:].zfill(8)   # Convert to 8-bit binary string
        return [int(bit) for bit in binary_string]      # Convert to list of integers
    if(isinstance(A, list)):
        byte_string = "".join(map(str, A))  # Convert bits to a string
        ascii_value = int(byte_string, 2)   # Convert binary string to integer
        return chr(ascii_value)             # Convert ASCII value to character

def encryption_decryption(message= None, key= None, mode= "encryption"):
    '''
    message: string for encryption mode. Ex "abc"\n
    message: list for decryption mode. Ex [0,1,0,0,0,0,0,1]\n
    key: list. Ex [0, 1]\n
    mode: string, Ex "encryption" / "decryption"
    '''
    if(message is not None and key is not None and len(key) > 0):
        ascii_len = 8
        k = 0   # for key
        if(mode == "encryption" and isinstance(message, str)):
            e = 0
            encryp_bits = []
            while(e < len(message)):
                bin_list = encrypter_decrypter(A= message[e])
                # Use key
                for i in range(ascii_len):
                    bin_list[i] = bin_list[i] ^ key[k]
                    k = (k + 1) % (len(key))
                #
                encryp_bits.extend(bin_list)
                e += 1
            return encryp_bits
        elif(mode == "decryption" and isinstance(message, list)):
            d = 0
            decryp_message = ""
            while(d < len(message)):
                bin_list = message[d: d + 8]
                # Use key
                for i in range(ascii_len):
                    bin_list[i] = bin_list[i] ^ key[k]
                    k = (k + 1) % (len(key))
                #
                decryp_message += encrypter_decrypter(A= bin_list)
                d += 8
            return decryp_message
        else:
            print("invalid Parameters")
            return None
    else:
        print("invalid message or key")
        return None
