import json

def markov(alphabet, database):
    #prepare table
    table = {}
    count = {}
    for char in alphabet:
        count[char] = 0
        for char2 in alphabet:
            table[char+char2] = 0

    #con markox model
    for data in database:
        for i in range(len(data)-1):
            table[data[i]+data[i+1]] +=1

    #count occurrence
    for data in database:
        for i in range(len(data)):
            count[data[i]] +=1

    for char in alphabet:
        for char2 in alphabet:
            if table[char+char2] != 0:
                table[char+char2] /= count[char]
            else:
                table.pop(char+char2, None)

    return table

def markov2(alphabet, database):
    #prepare table
    table = {}
    count = {}
    for char in alphabet:
        for char2 in alphabet:
            count[char+char2] = 0
            for char3 in alphabet:
                table[char+char2+char3] = 0

    #con markox model
    for data in database:
        for i in range(len(data)-2):
            table[data[i]+data[i+1]+data[i+2]] +=1

    #count occurrence
    for data in database:
        for i in range(len(data)-1):
            count[data[i]+data[i+1]] +=1

    for char in alphabet:
        for char2 in alphabet:
            for char3 in alphabet:
                if table[char+char2+char3] != 0:
                    table[char+char2+char3] /= count[char+char2]
                else:
                    table.pop(char+char2+char3, None)

    return table

result_1 = (markov('s0123t', ['s1331t','s2303t', 's1301t', 's2320t', 's1312t', 's1330t', 's1203t', 's1033t', 's2332t', 's2323t']))
result_2 = (markov2('s0123t', ['s1331t','s2303t', 's1301t', 's2320t', 's1312t', 's1330t', 's1203t', 's1033t', 's2332t', 's2323t']))


with open('markov.json', 'w') as fp:
    json.dump(result_1, fp, indent=4)
    json.dump(result_2, fp, indent=4)
