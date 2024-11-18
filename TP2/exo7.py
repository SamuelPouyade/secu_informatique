import socket
import string
import sys


def connect_to_server(server="51.195.253.124", port=4321) -> socket:
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        exit(1)

    return ma_socket


def attack_server(iterations: int, connection_method) -> list[str]:
    data = []

    for _ in range(iterations):
        soc = connection_method()
        data.append(soc.recv(1024).decode('utf_8').strip())
        soc.close()

    return data


def bad_vigenere_decrypting(iterations=1000, connection_method=connect_to_server) -> str:
    cypher_collection = attack_server(iterations, connection_method)

    plain_text = []
    for i in range(len(cypher_collection[0])):
        # On ne récupère qu'une seule lettre sur celles présentes
        letter_list = list(dict.fromkeys([cypher[i] for cypher in cypher_collection]))

        missing_letter = set(letter_list) ^ set(string.ascii_uppercase)

        if len(missing_letter) > 1:
            print(f"L'emplacement {i + 1} du message a plusieurs occurrences possibles : {missing_letter}")
            print("Merci de bien vouloir réessayer avec peut-être un nombre de requête plus important...")
            sys.exit(1)

        plain_text.append(missing_letter)

    return ''.join([''.join(sorted(list(s))) for s in plain_text])


def main() -> None:
    print(bad_vigenere_decrypting())


if __name__ == "__main__":
    main()
