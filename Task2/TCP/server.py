from socket import *

serverPort = 7019       # SID: 1231019 -> 7000 + 019 = 7019

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("TCP Server is listening on port", serverPort)

connectionSocket, addr = serverSocket.accept()
print("Connected by", addr)

messageCount = 0

while True:
    message = connectionSocket.recv(1024).decode()

    if not message:
        break

    print("Received:", message)

    messageCount += 1
    ackMessage = "ACK" + str(messageCount)

    connectionSocket.send(ackMessage.encode())
    print("Sent:", ackMessage)

    if message == "DONE":
        break

print("Total messages received:", messageCount)

connectionSocket.close()
serverSocket.close()