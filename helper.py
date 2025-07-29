import pickle as pk
from qiskit import QuantumCircuit
import random as rd

MESSAGE_BITS = (0, 1)
EMPTY= -1
POSSIBLE_BASES = ['H', 'D']

POSSIBLE_GATES = ['x', 'h', 'z', 'cx']

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

def encrypter_decrypter(A = "", L = []):
    if(L == []):
        ascii_value = ord(A)  # Get the ASCII value of the character
        binary_string = bin(ascii_value)[2:].zfill(8)   # Convert to 8-bit binary string
        return [int(bit) for bit in binary_string]      # Convert to list of integers
    if(A == ""):
        byte_string = "".join(map(str, L))  # Convert bits to a string
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
                decryp_message += encrypter_decrypter(L= bin_list)
                d += 8
            return decryp_message
        else:
            print("invalid Parameters")
            return None
    else:
        print("invalid message or key")
        return None

answer_file = 'answer.bin'

class grader:
    def __init__(self):
        self.__score = 0
        self.__answer_list = {}
        self.__task_flag = False
        self.set_person()

    def set_person(self, name= "", rollno = ""):
        self.name = "Agent " + name
        self.rollno = rollno

    def display(self):
        print(f"{self.name} Advanced to next level.\nCurrent score: {self.__score} / 6")
        self.file_dump()

    def intro_message(self):
        print(f'''
Welcome {self.name},
You have been given the task of Creating an Encryption device for message transmissions.
Use the Quantum cryptography for a secure channel.
Help Agent A and Agent B communicate the secret code.
All The best!
''')

    def ans_dump(self, qkd_name):
        self.__answer_list[0] = (self.name, self.rollno)
        with open(qkd_name + answer_file, 'wb') as fp:
            pk.dump(self.__answer_list, fp)

    def check_task(self, obj, i):
        if(self.__task_flag):
            if(i not in self.__answer_list):
                self.__score += 1
                self.__answer_list[i] = obj
            print(f"Good Job {self.name}🕵️. You passed.✅")
        else:
          print("Try Again.🔄")    
        print("Your score: ", self.__score)    

# For B92
class B92(grader):
    def __init__(self):
        super().__init__()

    def file_dump(self):
        self.ans_dump("B92_")

    def Q1(self, qc: QuantumCircuit, bits: list):
        self.__task_flag = True

        qcInstructions = qc.data

        # Only barrier is wrong if 1 present
        if(len(qcInstructions) == 1 and 1 in bits):
            self.__task_flag = False

        for qcInstruction in qcInstructions:
            # print(qcInstruction)

            if(qcInstruction.name == POSSIBLE_GATES[1]):
                qIndex = qcInstruction.qubits[0]._index
                # print(qIndex)

                if(bits[qIndex] != MESSAGE_BITS[1]):
                    print('Wrong encoding.')
                    self.__task_flag = False
                    break
            elif(qcInstruction.name != 'barrier'):
                print(f'Wrong {qcInstruction.name} gate.')
                self.__task_flag = False
                break

        self.check_task((bits), 1)

    def Q2(self, qc: QuantumCircuit, bases: list):
        self.__task_flag = True

        temp_bases = list([EMPTY] * len(bases))
        barrier_found = False
        qcInstructions = qc.data

        for qcInstruction in qcInstructions:
            # print(qcInstruction)

            if(qcInstruction.name == 'barrier' or barrier_found):
                if(qcInstruction.name == POSSIBLE_GATES[1]):
                    qIndex = qcInstruction.qubits[0]._index
                    # print(qIndex)

                    if(bases[qIndex] != POSSIBLE_BASES[1] or temp_bases[qIndex] == bases[qIndex]):
                        self.__task_flag = False
                        break
                    temp_bases[qIndex] = POSSIBLE_BASES[1]

                elif(qcInstruction.name != 'barrier'):
                    print(f'Wrong {qcInstruction.name} gate.')
                    self.__task_flag = False
                    break

                if(not barrier_found):
                    barrier_found = True
                elif(qcInstruction.name == 'barrier' and barrier_found):
                    if(POSSIBLE_BASES[1] in bases and POSSIBLE_BASES[1] not in temp_bases):
                        print("Error in bases and gates")
                        self.__task_flag = False
                    break

        self.check_task((bases), 2)

    def Q3(self, count_dict: dict, key_string: str):
        key_strings = tuple(count_dict.keys())
        # print(key_strings)

        if(key_string in key_strings):
            self.__task_flag = True
        else:
            self.__task_flag = False
        self.check_task((key_strings, key_string), 3)

    def Q4(self, unity_indexes: list, bits: list):
        self.__task_flag = True

        if(len(unity_indexes) == 0):
            print("Re-run for Non-EMPTYu_index key.")
            self.__task_flag = False

        for index in unity_indexes:
            if(index > len(bits) or bits[index] == EMPTY):
                self.__task_flag = False
                break

        self.check_task((unity_indexes, bits), 4)

    def Q5(self, function):
        self.__task_flag = True
        test_case1 = [0,0,0,0,0]
        test_case2 = [1,1,1,1,1]
        test_case3 = [0,0,0,0,1]
        test_case4 = [0,1,0,1,0]

        tests = (
            (test_case1, test_case1, True),
            (test_case2, test_case2, True),
            (test_case1, test_case3, True),
            (test_case2, test_case4, False),
            (test_case3, test_case4, False)
        )

        for test_case in tests:
            A,B,V = test_case
            if(function(A, B) != V):
                self.__task_flag = False
                break

        self.check_task((), 5)

    def Q6(self, key_1: list, key_2: list):
        if(key_1 == key_2):
            self.__task_flag = True
        else:
            self.__task_flag = False
        self.check_task((key_1, key_2), 6)
