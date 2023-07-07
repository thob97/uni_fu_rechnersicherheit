import logging
log = ''

loggers = {}
def new_log(name, level = logging.INFO):
    #if logger already exists
    global loggers
    if loggers.get(name):
        return loggers.get(name)

    log = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    fileHandler = logging.FileHandler(f'log/{name}.log')
    fileHandler.setFormatter(formatter)
    streamHandler = logging.StreamHandler()
    streamHandler.setFormatter(formatter)

    log.setLevel(level)
    log.addHandler(fileHandler)
    log.addHandler(streamHandler)
    loggers[name] = log
    return log

log = new_log('log', logging.INFO)

def pm_user_log(log_msg, username_1, username_2):
    #sort the usernames and then join them to one filename
    filename = ''.join( sorted( (username_1, username_2) ) )
    log = new_log(filename)
    log.info(log_msg)

def log_to_file(log_name_1, log_name_2):
    if log_name_2 == None:
        with open('log/log.log', 'rb') as file:
            return file.read()
    
    else:
        filename = ''.join( sorted( (log_name_1, log_name_2) ) )
        filename = f'log/{filename}.log'
        try:
            with open(filename, 'rb') as file:
                return file.read()
        except:
            return b'No such history'