import hashlib
import string
import json
import time
import threading

#TASK_SIZE is the size in which the task will be split ~ numThreads
TASK_SIZE = 16
string_alphabet  = string.ascii_lowercase + string.ascii_uppercase + '0123456789'
alphabet = list(string_alphabet)
dict = {}

class myThread(threading.Thread):
    def __init__(self, tid, task):
        threading.Thread.__init__(self)
        self.lock = threading.Lock()
        self.tid = tid
        self.task = task
        
    def run(self):
        #password test each possible combination of alphabet with 4 chars
        for char1 in self.task:
            for char2 in alphabet:
                for char3 in alphabet:
                    for char4 in alphabet:
                        password = char1 + char2 + char3 + char4
                        salt = seed+password
                        hash = hashlib.sha256(salt.encode()).hexdigest()
                        try:
                            test = dict[hash]
                            #print(hash, password)
                            with self.lock:
                                dict[hash] = password
                            
                        except:
                            pass


if __name__ == "__main__":
    start_time = time.time()

    #create dictonary of file
    seed = ''
    with open("sha2pwd.txt", "r") as file:
        #strip unnecessary leading and ending chars
        seed = file.readline().lstrip("Seed: ").rstrip("\n")
        for line in file:
            hash = line.rstrip("\n")
            dict[hash] = 0

    #split into qeual tasks of size TASK_SIZE for threads
    tasks = []
    single_task = []
    for char in string_alphabet:
        single_task.append(char)
        if len(single_task) == TASK_SIZE:
            tasks.append(single_task)
            single_task = []
    if single_task != []:
        tasks.append(single_task)

    #start threads
    thread_list = []
    for i in range(len(tasks)):
        worker_thread = myThread(i,tasks[i])
        worker_thread.start()
        thread_list.append(worker_thread)

    #wait for all threads to finish
    for thread in thread_list:
        thread.join()

    #result to file
    with open('result_multi_threading.txt', 'w') as file:
        file.write(json.dumps(dict)) 

    #print execution time
    print("--- %s seconds ---" % (time.time() - start_time))