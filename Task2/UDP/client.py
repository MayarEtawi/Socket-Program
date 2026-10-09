from socket import *
import time

serverName = gethostname()
serverPort = 7200       # SID: 1230199 -> 7001 + 199 = 7200

clientSocket = socket(AF_INET, SOCK_DGRAM)

for i in range (1,201):
    message = "Packet-" + str(i)
    clientSocket.sendto(message.encode(), (serverName, serverPort))   
    print("Packet Sent: ", message)
    time.sleep(0.1)

 
clientSocket.close()