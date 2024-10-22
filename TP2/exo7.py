import socket
import sys


def connect_to_server(server="51.195.253.124", port=4321) -> socket:
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        exit(1)

    return ma_socket

def spam_queries(spam_rate=1000) -> list[str]:
    data = []

    for _ in range(spam_rate):
        soc = connect_to_server()
        data.append(soc.recv(1024).decode('utf_8').strip())
        soc.close()

    return data


def get_alphabet() -> list[chr]:
    """
    Fonction pour récupérer les lettres de l'alphabet latin en majuscule
    :return: la liste des lettres majuscules
    """
    return [chr(ord('A') + i) for i in range(26)]


if __name__ == "__main__":
    cypher_collection = spam_queries(300)

    plain_text = []
    for i in range(len(cypher_collection[0])):
        # On ne recupere qu'une seule lettre sur celles presentes
        letter_list = list(dict.fromkeys([cypher[i] for cypher in cypher_collection]))

        missing_letter = set(letter_list) ^ set(get_alphabet())

        if len(missing_letter) > 1:
            print(f"L'emplacement {i + 1} du message a plusieurs occurrences possibles : {missing_letter}")
            print("Merci de bien vouloir réessayer avec peut-être un nombre de requête plus important...")
            sys.exit(1)

        plain_text.append(missing_letter)

    plain_text = [''.join(sorted(list(s))) for s in plain_text]

    print(''.join(plain_text))



