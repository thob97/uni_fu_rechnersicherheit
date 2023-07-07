import hashlib
import string
import json

#alphabet
string_alphabet  = string.ascii_lowercase + string.ascii_uppercase + '0123456789'
alphabet = list(string_alphabet)

#create dictonary of file
dict = {}
seed = ''
with open("sha2pwd.txt", "r") as file:
    #strip unnecessary leading and ending chars
    seed = file.readline().lstrip("Seed: ").rstrip("\n")
    for line in file:
        hash = line.rstrip("\n")
        dict[hash] = 0

#password test each possible combination of alphabet with 4 chars
for char1 in alphabet:
    for char2 in alphabet:
        for char3 in alphabet:
            for char4 in alphabet:
                password = char1 + char2 + char3 + char4
                salt = seed+password
                hash = hashlib.sha256(salt.encode()).hexdigest()
                try:
                    test = dict[hash]
                    dict[hash] = password
                    #print(hash, password)
                except:
                    pass

#result to file
with open('result_single_process.txt', 'w') as file:
     file.write(json.dumps(dict)) 
