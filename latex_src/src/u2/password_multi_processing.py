import hashlib
import string
import json
import time
from multiprocessing import Process, Lock

PROCESSES = int(input('enter number of processes: '))
string_alphabet  = string.ascii_lowercase + string.ascii_uppercase + '0123456789'
TASK_SIZE = len(string_alphabet)//PROCESSES  
alphabet = list(string_alphabet)
password_dict = {}
seed = ''
lock = Lock()

def run(tid, task):
    #password test each possible combination of alphabet with 4 chars
    for char1 in task:
        for char2 in alphabet:
            for char3 in alphabet:
                for char4 in alphabet:
                    password = char1 + char2 + char3 + char4
                    salt = seed+password
                    hash = hashlib.sha256(salt.encode()).hexdigest()
                    try:
                        test = password_dict[hash]
                        #print(hash, password)
                        with lock:
                            password_dict[hash] = password
                    except:
                        pass

def main():

    start_time = time.time()

    with open("sha2pwd.txt", "r") as file:
        #strip unnecessary leading and ending chars
        seed = file.readline().lstrip("Seed: ").rstrip("\n")
        for line in file:
            hash = line.rstrip("\n")
            password_dict[hash] = 0

    #split into qeual tasks of size TASK_SIZE for processes
    tasks = []
    single_task = []
    for char in string_alphabet:
        single_task.append(char)
        if len(single_task) == TASK_SIZE:
            tasks.append(single_task)
            single_task = []
    if single_task != []:
        tasks[-1] = tasks[-1] + single_task

    #start processes
    process_list = []
    for i in range(len(tasks)):
        process = Process(target=run, args=(i, tasks[i]))
        process.start()
        process_list.append(process)

    #wait for all threads to finish
    for process in process_list:
        process.join()

    #result to file
    with open('result.txt', 'w') as file:
        file.write(json.dumps(password_dict)) 

    #print execution time
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == "__main__":
    main()