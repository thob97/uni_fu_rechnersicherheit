import os
import hashlib
import random, time


class UserManager:

    def __init__(self):
        self.__path = os.path.dirname(os.path.abspath(__file__))
        self.__config = "config"
        self.__usrfile = "passwd"
        self.__pwdfile = "shadow"
        self.__idcount = 0
        self.__loadcfg()
        open(os.path.join(self.__path, self.__config), 'a').close()
        open(os.path.join(self.__path, self.__usrfile), 'a').close()
        open(os.path.join(self.__path, self.__pwdfile), 'a').close()

    # load last state
    def __loadcfg(self):
        # config present or first start?
        if os.path.exists(os.path.join(self.__path, self.__config)):
            file = open(os.path.join(self.__path, self.__config))
            for line in file:
                line = line.strip()
                content = line.split(':')
                if content[0] == "id":
                    self.__idcount = int(content[1])
            file.close()

    # save last state
    def __savecfg(self):
        tempfile = open(os.path.join(self.__path, "temp"))
        tempfile.write("id:")+self.__idcount
        tempfile.close()
        os.replace(os.path.join(self.__path, self.__config), os.path.join(self.__path, "temp"))

    # add a new user with the given password
    # 0 - success
    # 1 - error: user already exists
    def useradd(self, name, passwd):
        file = open(os.path.join(self.__path, self.__usrfile), "r+")
        for line in file:
            line = line.strip()
            content = line.split(':')
            if content[1] == name:
                file.close()
                return 1, []
        print('received new account data...')
        time.sleep(10)
        print('now writing data to log!')
        file.write(str(self.__idcount)+":"+name+":1\n")
        file.close()
        self.passwd(self.__idcount, passwd, "n")
        del passwd
        self.__idcount += 1
        return 0, [self.__idcount-1, 1]

    # remove the specified user
    # 0 - success
    # 1 - error: user does not exist
    def userdel(self, userid):
        tempfile = open(os.path.join(self.__path, "temp"), "w")
        file = open(os.path.join(self.__path, self.__usrfile), "r")
        exists = False
        for line in file:
            if exists:
                line = line.strip()
                content = line.split(':')
                if content[0] == str(userid):
                    exists = True
                else:
                    tempfile.write(line+"\n")
            else:
                tempfile.write(line)
        file.close()
        tempfile.close()
        if not exists:
            os.remove(os.path.join(self.__path, "temp"))
            return 1
        else:
            os.replace(os.path.join(self.__path, self.__usrfile), os.path.join(self.__path, "temp"))
            tempfile = open(os.path.join(self.__path, "temp"), "w")
            file = open(os.path.join(self.__path, self.__pwdfile), "r")
            exists = False
            for line in file:
                if exists:
                    line = line.strip()
                    content = line.split(':')
                    if content[0] == str(userid):
                        exists = True
                    else:
                        tempfile.write(line + "\n")
                else:
                    tempfile.write(line)
            file.close()
            tempfile.close()
            os.replace(os.path.join(self.__path, self.__pwdfile), os.path.join(self.__path, "temp"))
        return 0

    # login a user
    # 0, [id, perm] - success
    # 1, [] - error: wrong username or password
    def login(self, username, passwd):
        uid = -1
        perm = -1
        file = open(os.path.join(self.__path, self.__usrfile), "r")
        for line in file:
            line = line.strip()
            content = line.split(':')
            if content[1] == username:
                uid = int(content[0])
                perm = int(content[2])
                break
        file.close()
        if uid == -1:
            return 1, []
        controlhash = ""
        passwdhash = ""
        file = open(os.path.join(self.__path, self.__pwdfile), "r")
        for line in file:
            line = line.strip()
            content = line.split(':')
            if int(content[0]) == uid:
                salt = content[1]
                controlhash = content[2]
                passwdhash = hashlib.md5((salt + passwd).encode('utf-8')).hexdigest()
                break
        file.close()
        if controlhash != "" and passwdhash != "" and controlhash == passwdhash:
            return 0, [uid, perm]
        else:
            return 1, []

    # save the configuration and close
    def close(self):
        self.__savecfg()
        return

    # set the given password for the given user
    # n = new
    # r = replace
    def passwd(self, userid, passwd, flag="n"):
        salt = self.__getsalt()
        passwdhash = hashlib.md5((salt + passwd).encode('utf-8')).hexdigest()
        del passwd
        # append new password to the file
        if flag == "n":
            file = open(os.path.join(self.__path, self.__pwdfile), "w")
            newline = str(userid)+":"+salt+":"+passwdhash+"\n"
            file.write(newline)
            file.close()

        # replace the password for an existing user
        elif flag == "r":
            tempfile = open(os.path.join(self.__path, "temp"), "w")
            file = open(os.path.join(self.__path, self.__pwdfile), "r")
            exists = False
            for line in file:
                if not exists:
                    line = line.strip()
                    content = line.split(':')
                    if content[0] == userid:
                        exists = True
                        content[1] = salt
                        content[2] = passwdhash
                        newline = ""
                        for i in range(len(content)):
                            if i != len(content)-1:
                                newline += content[i]+":"
                            else:
                                newline += content[i]+"\n"
                        tempfile.write(line+"\n")
                    else:
                        tempfile.write(line+"\n")
                else:
                    tempfile.write(line)

            # user does not exist
            # TO TO: throw error that the user doesnt exist
            if not exists:
                tempfile.writelines(file.readlines())
            file.close()
            tempfile.close()
            os.replace(os.path.join(self.__path, self.__pwdfile), os.path.join(self.__path, "temp"))

    # get a random salt
    def __getsalt(self):
        salt = ""
        length = random.randint(8, 15)
        for i in range(length):
            # get random char except ':'
            next_char = ':'
            while next_char == ':':
                next_char = chr(random.randint(33, 127))
            salt += next_char
        return salt
