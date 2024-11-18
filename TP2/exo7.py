import socket
import string
import sys

from tqdm import trange

def connect_to_server(server="51.195.253.124", port=4321) -> socket.socket:
    """
    Se connecte au serveur ayant la mauvaise implémentation du chiffrement de Vernam
    :param server: Adresse du serveur (51.195.253.124 par défaut)
    :type server: str
    :param port: Port du serveur (4321 par défaut)
    :type port: int
    :return: Socket de connexion au serveur
    :rtype: socket.socket
    """
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        exit(1)

    return ma_socket


def query_server(iterations: int, connection_method) -> list[str]:
    """
    Requête un serveur pour récupérer un jeu de données
    :param iterations: Nombre de requêtes à effectuer
    :type iterations: int
    :param connection_method: Méthode de connexion au serveur
    :type connection_method: () -> socket.socket
    :return: Liste des données récupérées
    :rtype: list[str]
    """
    data = []

    for _ in trange(iterations, desc="Récupération des données ", unit="requête"):
        soc = connection_method()
        data.append(soc.recv(1024).decode('utf_8').strip())
        soc.close()

    return data


def bad_vernam_decrypting(iterations=1000, connection_method=connect_to_server) -> str:
    """
    Décrypte un message chiffré avec un chiffrement de Vernam mal implémenté
    :param iterations: Nombre de requêtes à effectuer auprès du serveur
    :type iterations: int
    :param connection_method: Méthode de connexion au serveur
    :type connection_method: () -> socket.socket
    :return: Message décrypté
    :rtype: str
    """
    cypher_collection = query_server(iterations, connection_method)

    plain_text = []
    # Itération sur chaque lettre
    for i in range(len(cypher_collection[0])):
        # On ne récupère qu'une seule lettre sur toutes celles présentes
        letter_list = set(dict.fromkeys([cypher[i].upper() for cypher in cypher_collection]))

        # On récupère la liste des lettres manquantes en XORant l'alphabet
        missing_letter = list(letter_list ^ set(string.ascii_uppercase))

        # Si plus d'une lettre est manquante, on retourne une erreur
        if len(missing_letter) > 1:
            raise ValueError(f"L'emplacement {i + 1} du message a plusieurs occurrences possibles : {missing_letter}"
                             + "Merci de bien vouloir réessayer avec un nombre de requête plus important.")

        plain_text.append(missing_letter[0])

    # On convertit la liste de lettres en chaîne de caractères avant de la retourner
    return ''.join(plain_text)


def main() -> None:
    print(bad_vernam_decrypting(300))


if __name__ == "__main__":
    main()
