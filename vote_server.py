# Server to implement simple program to get votes tallied from two different
# clients. The server will wait until two different clients connect, before
#  sending a message down to each client.
# Author: fokumdt 2019-09-26
# Version: 0.1
#!/usr/bin/python3

import socket
import sys

def clientACK():
    """Generates client acknowledgment"""
    status = "200 OK"
    return status

def candidatesHello(str1, str2):
    """Generates client hello message"""
    status = "105 Candidates " + str1 + " " + str2
    return status
        
def WinnerMsg(strWinner, votes):
    """Sends message with winner identified"""
    status = "220 Winner " + strWinner + " " + str(votes)
    return status

def RunnerUpMsg(strRunnerUp, votes):
    """Sends message with runner-up identified"""
    status = "221 Runner-up " + strRunnerUp + " " + str(votes)
    return status

# s      = socket
# msg     = initial message being processed
# state  = dictionary containing state variables
def processMsgs(s, msg, state):
    """This function processes messages that are read through the socket. It
        returns a status, which is an integer indicating whether the operation
        was successful"""
    if(msg[:3] == "100"):
            print(msg)
            conn, addr = s.accept()
            if(conn != None):
                print('Connected by', addr)
                state["client2"] = conn
            msg = conn.recv(1024).decode('utf-8')
            print(msg)
            state["client1"].send(str.encode(candidatesHello(
                state["candidate1"], state["candidate2"])))
            state["client2"].send(str.encode(candidatesHello(
                state["candidate1"], state["candidate2"])))
            return 1

    """Checking for the second client"""
    if(msg[:3]=="110"):
        castedvote = msg[9:]
        if(castedvote == state["candidate1"]):
            state["votec1"]+=1
        elif (castedvote == state["candidate2"]):
            state["votec2"] += 1
        state["client1"].send(str.encode(clientACK()))

        """Checking for the second client"""
        msg = state["client2"].recv(1024).decode('utf-8')
        if(msg[:3]=="110"):
            castedvote = msg[9:]
            if(castedvote == state["candidate1"]):
                state["votec1"] += 1
            elif (castedvote == state["candidate2"]):
                state["votec2"] += 1
            state["client2"].send(str.encode(clientACK()))
            return 1
        else:
            msg = "120"
        
    
    if(msg[:3] == "120"):
        if(state["votec1"] > state["votec2"]):
            state["client1"].send(str.encode(WinnerMsg(state["candidate1"], state["votec1"])))
            state["client1"].send(str.encode(RunnerUpMsg(state["candidate2"], state["votec2"])))
            msg = state["client2"].recv(1024).decode('utf-8')
            state["client2"].send(str.encode(WinnerMsg(state["candidate1"], state["votec1"])))
            state["client2"].send(str.encode(RunnerUpMsg(state["candidate2"], state["votec2"])))
        else:
            state["client1"].send(str.encode(WinnerMsg(state["candidate2"], state["votec2"])))
            state["client1"].send(str.encode(RunnerUpMsg(state["candidate1"], state["votec1"])))
            msg = state["client2"].recv(1024).decode('utf-8')
            state["client2"].send(str.encode(WinnerMsg(state["candidate2"], state["votec2"])))
            state["client2"].send(str.encode(RunnerUpMsg(state["candidate1"], state["votec1"])))
        return 1

    return 0

def main():
    """Driver function for the project"""
    args = sys.argv

    if len(args) != 2:
        print ("Please supply a server port.")
        sys.exit()

    state={"client1":None,"client2":None,"votec1":0, "votec2":0}
    print("Enter Candidate One Name: ")
    state["candidate1"] = input()
    print("Enter Candidate Two Name: ")
    state["candidate2"] = input()

    HOST = 'localhost'      # Symbolic name meaning all available interfaces
    PORT = int(args[1])     # The port on which the server is listening
    if PORT < 1023 or PORT > 65535:
        print("Invalid port specified.")
        sys.exit()
        
    print("Server of Kimberly Stewart")        
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        # Bind socket
        s.bind((socket.gethostbyname(HOST),PORT));
        # listen
        s.listen(1)
        conn, addr = s.accept()#accept connection using socket
        with conn:
            state["client1"] =  conn
            print('Connected by', addr)
            status = 1
            while (status==1):
                msg = conn.recv(1024).decode('utf-8')
                if not msg:
                    status = -1
                else:
                    status = processMsgs(s, msg, state)
            if status < 0:
                print("Invalid data received. Closing")
            conn.close()
            print("Closed connection socket")

if __name__ == "__main__":
    main()
