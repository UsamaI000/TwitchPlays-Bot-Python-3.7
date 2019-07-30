import threading
import random
import time
import socket
import pyautogui
from directkeys import PressKey, ReleaseKey, W, A, S, D
import configparser


config = './config.ini'
cparser = configparser.ConfigParser()
cparser.read(config)
SERVER = cparser['AUTH']['SERVER']
PORT = int(cparser['AUTH']['PORT'])
PASS = cparser['AUTH']['PASS']
BOT = cparser['AUTH']['BOT']
CHANNEL = cparser['AUTH']['CHANNEL']
OWNER = cparser['AUTH']['OWNER']


irc = socket.socket()
irc.connect((SERVER, PORT))
irc.send(("PASS " + PASS + "\n" + "nick " + BOT + "\n" + "JOIN #" + CHANNEL + "\n").encode())
message = ''

def gameControls():
    global message 
    while True:
        if 'w' in message.lower():
            PressKey(W)
            message = ""
            time.sleep(2)
            ReleaseKey(W)
            
        elif 's' in message.lower():
            PressKey(S)
            message = ""
            time.sleep(2)
            ReleaseKey(S)
            
        elif 'a' in message.lower():
            PressKey(A)            
            message = ""
            time.sleep(2)
            ReleaseKey(A) 
             
        elif 'd' in message.lower():
            PressKey(D)
            message = ""
            time.sleep(2)
            ReleaseKey(D)
            
        else:
            pass


def twitch():
    def joinchat():
        loading = True
        while loading:
            readBuffer_join = irc.recv(1024)
            readBuffer_join = readBuffer_join.decode()
            for line in readBuffer_join.split("\n")[0:2]:
                print(line)
                loading = loadingComplete(line)
                
    def loadingComplete(line):
        if ("End of /NAMES list" in line):
            print("Bot has Joined " + CHANNEL + " a channel")
            sendMessage(irc, "Chat room joined")
            return False
        else:
            return True

    def sendMessage(irc, message):
        messageTemp = "PRIVMSG #" + CHANNEL + " :" + message
        irc.send((messageTemp + "\n").encode()) 

    def getUser(line):
        separate = line.split(":", 2)
        user = separate[1].split("!", 1)[0]
        return user

    def getMessage(line):
        global message
        try:
            message = (line.split(":", 2))[2]
        except:
            message = ""
        return message

    def console(line):
        if "PRIVMSG" in line:
            return False
        else:
            return True

    joinchat()        

    while True:
        try:
            readBuffer = irc.recv(1024).decode()
        except:
            readBuffer = ""
        for line in readBuffer.split("\r\n"):
            if line == "":
                continue
            elif "PING" in line and console(line):
                msgg = "PONG tmi.twitch.tv\r\n".encode()
                irc.send((msgg))
                print(msgg)
                continue
            else:
                user = getUser(line)
                message = getMessage(line)
                print(user + ": " + message)

if __name__ == "__main__":
    t1 = threading.Thread(target= twitch)
    t1.start()
    t2 = threading.Thread(target= gameControls)
    t2.start()    
    