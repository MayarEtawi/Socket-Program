from socket import *
import time

serverName = gethostname()
serverPort = 7019       # SID: 1231019 -> 7000 + 019 = 7019

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

messages = ["HELLO SERVER"]

for i in range(1, 11):
    messages.append("Message " + str(i))

messages.append("DONE")

for message in messages:
    clientSocket.send(message.encode())
    print("Sent:", message)

    ackMessage = clientSocket.recv(1024).decode()
    print("Received from server:", ackMessage)

    time.sleep(0.5)

clientSocket.close()