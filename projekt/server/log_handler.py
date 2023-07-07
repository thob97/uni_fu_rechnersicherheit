import logging
import sys
from classes import Header
sys_log = ''
log_directory = 'system_files/log/'
system_log = 'system_files/sys_log.log'
global_log = 'system_files/global_log.log'

private_msg = 'pm'
send_file_command = 'send_file'

loggers = {}
def new_log(name, level = logging.INFO):
    #if logger already exists
    global loggers
    if loggers.get(name):
        return loggers.get(name)

    #else logger settings
    log = logging.getLogger(name)
    formatter = logging.Formatter('%(asctime)s:%(levelname)s:%(message)s')
    fileHandler = logging.FileHandler(name)
    fileHandler.setFormatter(formatter)

    #only stdout for systemlog
    if name == system_log:
        streamHandler = logging.StreamHandler(stream=sys.stdout)
        streamHandler.setFormatter(formatter)
        log.addHandler(streamHandler)

    log.setLevel(level)
    log.addHandler(fileHandler)
    loggers[name] = log
    return log

sys_log = new_log(system_log)

def handle_commands(username, data):
    msg_header = Header().return_header(data)
    command, option, msg = msg_header.get_information()

    #We dont want to see the send_file in log
    if command == send_file_command:
        msg = option

    log_msg = f'USER:{username}:CMD:{command}:OPT:{option}:MSG:{msg}'
    
    #Always write to system log
    log = new_log(system_log)
    log.info(log_msg)

    #if its a pm
    if command == private_msg:
        #join the usernames to one filename
        #sort the usernames so that two users fill always have the same file
        filename = ''.join( sorted( (username, option) ) )
        file_directory = f'{log_directory}{filename}.log'
        log = new_log(file_directory)
        log.info(log_msg)

    else:
        #if its not an pm also write to global log
        log = new_log(global_log)
        log.info(log_msg)


def log_to_file(username_1, option):
    if option == 'global':
        with open(global_log, 'rb') as file:
            return file.read()

    #option is a username
    else:
        #get the filename of the users log file
        filename = ''.join( sorted( (username_1, option) ) )
        filename = f'{log_directory}{filename}.log'
        try:
            with open(filename, 'rb') as file:
                return file.read()
        except:
            return b'System: No such history'