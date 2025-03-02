import pickle as pk
from qiskit import QuantumCircuit

message_bits = (0, 1)
possible_bases = ['H', 'D']

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

class QQ2grader:
    def __init__(self):
        self.__score = 0
        self.__answer_list = {}
        self.__task_flag = False
        self.set_person()

    def set_person(self, name= "", rollno = ""):
        self.name = "Agent " + name
        self.rollno = rollno

    def display(self):
        print(f"{self.name} Advanced to next level.\nCurrent score: {self.__score}")

    def intro_message(self):
        print(f'''
Welcome {self.name},
You have been given the task of Creating an Encryption device for message transmissions.
Use the Quantum cryptography for a secure channel.
Help Agent A and Agent B communicate the secret code.
All The best!
''')

    def file_dump(self):
        if(self.__answer_list != {}):
            with open(answer_file, "wb") as fp:
                pk.dump(fp, self.__answer_list)

    def check_task(self, obj, i):
        if(self.__task_flag):
            if(i not in self.__answer_list):
                self.__score += 1
                self.__answer_list[i] = obj
            print(f"Good Job {self.name}🕵️. You passed.✅")
        else:
          print("Try Again.🔄")    
        print("Your score: ", self.__score)      

    def Q1(self, qc: QuantumCircuit, bits: list):
        pass

    def Q2(self, qc: QuantumCircuit, bases: list):
        pass

    def Q3(self, count_dict: dict, key_string: str):
        key_strings = tuple(count_dict.keys())
        # print(key_strings)

        if(key_string in key_strings):
            self.__task_flag = True
        else:
            self.__task_flag = False
        self.check_task((key_strings, key_string), 3)

    def Q4(self, unity_indexes: list, bits: list):
        pass

    def Q5(self, function):
        pass

    def Q6(self):
        pass