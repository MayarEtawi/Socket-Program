from socket import *

host = gethostname()
serverPort = 7200       # SID: 1230199 -> 7001 + 199 = 7200

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind((host, serverPort))
serverSocket.settimeout(10) # used to stop receiving after 10 seconds without packets

print("The server is ready to receive")

receivedPackets = []

while True:
    try:
        data, clientAddress = serverSocket.recvfrom(1024)
        message = data.decode()
        print("Received:", message)
        receivedPackets.append(message)

    except timeout:
        print("No more packets received.")
        break

numbers = []

for packet in receivedPackets:
    number = int(packet.split("-")[1])
    numbers.append(number)

missing = []

for i in range(1, 201):
    if i not in numbers:
        missing.append(i)

outOfOrder = 0

for i in range(1, len(numbers)):
    if numbers[i] < numbers[i - 1]:
        outOfOrder += 1

print("Total packets received:", len(numbers))
print("Number of missing packets:", len(missing))
print("Number of out-of-order packets:", outOfOrder)

serverSocket.close()