# Client to collect votes from a client and send them to a server.
# Author: fokumdt 2019-09-26
# Version: 0.1
#!/usr/bin/python3

import socket
import sys


def serverHello():
    """Generates server hello message"""
    status = "100 Hello"
    return status

def voteNotification(strCandidate):
    """Generates message to let server know of user selection."""
    status = "110 Vote " + strCandidate
    return status

def pollClosing():
    """Generates message to let server know of poll closing."""
    status = "120 Poll closed"
    return status

# s       = socket
# msg     = initial message being processed
# state   = dictionary containing state variables
def processMsgs(c, msg, state): 
    """This function processes messages that are read through the socket. 
    It returns a status, which is an integer indicating whether the operation was successful"""
    if(msg[:3] =="105"):
        print(msg)
        print("Please select the candidate to vote for: ")
        vote = input()
        c.send(str.encode(voteNotification(vote)))
        return 1
    
    if (msg[:3] == "200"):
        print("Would you like to cast another Vote? Enter Y/N ")
        choice = input()

        if(choice in ["y","Y"]):
            print("Please select the candidate to vote for: ")
            vote = input()
            c.send(str.encode(voteNotification(vote)))
            return 1
        else:
            c.send(str.encode(pollClosing()))
            return 1
    
    if(msg[:3]=="220"):
        print(msg)
        return 1
    if(msg[:3]=="221"):
        print(msg)
        return 0
    return 0

def main():
    """Driver function for the project"""
    args = sys.argv
    if len(args) != 4:
        print ("Please supply a server address and port.")
        sys.exit()
    serverHost = str(args[1])       # The remote host
    serverPort = int(args[2])  
    name = str(args[3])     # The same port as used by the server
    state={}
    print("Client "+name+" of Kimberly Stewart")
    # Add code to initialize the socket
    c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    msg = serverHello()
    # Add code to send data into the socket
    c.connect((serverHost,serverPort))
    c.send(str.encode(msg))
    # Handle the data that is read through the socket by using processMsgs(s, msg, state)
    status = 1
    while(status==1):
        msg = c.recv(1024).decode('utf-8')
        if not msg:
            status = -1
        else:
            status = processMsgs(c, msg, state)
        if status < 0:
                print("Invalid data received. Closing")
    # Close the socket.
if __name__ == "__main__":
    main()
