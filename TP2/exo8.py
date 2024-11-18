import socket
import sys

from Crypto.Cipher import AES


def connect_to_oracle(server="51.195.253.124", port=11111) -> socket:
    """
    Connexion à l'oracle
    :param server: Adresse IP du serveur
    :type server: str
    :param port: Port du serveur
    :type port: int
    :return: Socket de connexion
    :rtype: socket
    """
    soc_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc_con.connect((server, port))
    except Exception as e:
        print("Problème de connexion avec l'oracle", e.args)
        sys.exit(1)

    return soc_con


def is_valid_padding(soc: socket, cipher_block: str) -> bool:
    """
    Vérifie si le padding est valide grâce à l'oracle (serveur distant)
    :param soc: Socket de connexion à l'oracle
    :type soc: socket
    :param cipher_block: Bloc chiffré à tester
    :type cipher_block: str
    :return: True si le padding est valide, False sinon
    :rtype: bool
    """
    # Envoi des donnees
    soc.sendall(cipher_block.encode("utf-8"))

    # Enregistrement de la reponse
    ligne = soc.recv(1024)

    if ligne == b'Successfully decrypted.\n':
        return True

    return False


def decrypt_block(current_block: bytes, previous_block: bytes, connection: socket) -> bytearray:
    """
    Décrypte un bloc chiffré en utilisant la méthode du padding oracle
    :param connection: Socket de connexion à l'oracle
    :type connection: socket
    :param current_block: Bloc chiffré à déchiffrer
    :type current_block: bytes
    :param previous_block: Bloc précédent
    :type previous_block: bytes
    :return: Bloc en clair
    :rtype: bytearray
    """
    # Initialisation des variables
    buffer = bytearray(AES.block_size)
    plain_block = bytearray(AES.block_size)

    # Attaque sur chaque octet du bloc
    for block_cursor in range(AES.block_size - 1, -1, -1):
        # Test de chaque valeur possible
        for byte_value in range(256):
            buffer[block_cursor] = byte_value
            cipher_block_attack = buffer + current_block

            if is_valid_padding(connection, cipher_block_attack.hex()):
                # Calcul de l'octet en clair
                plain_byte = (AES.block_size - block_cursor) ^ previous_block[block_cursor] ^ byte_value
                plain_block[block_cursor] = plain_byte
                print(plain_block[block_cursor:])

                # Mise à jour du buffer pour le prochain padding
                for i in range(block_cursor, AES.block_size):
                    buffer[i] = (AES.block_size - block_cursor + 1) ^ plain_block[i] ^ previous_block[i]

                break

    return plain_block


def decrypt_via_padding_oracle(cipher: bytes, connection: socket) -> str:
    """
    Décrypte une donnée chiffrée avec AES-CBC utilisant du padding par la méthode
    du padding oracle
    :param cipher: Donnée chiffrée
    :type cipher: bytes
    :param connection: Socket de connexion à l'oracle
    :type connection: socket
    :return: Donnée en clair
    :rtype: str
    """
    # Découpage du texte chiffré en blocs
    cipher_blocks = [cipher[i * AES.block_size:(i + 1) * AES.block_size] for i in range(len(cipher) // AES.block_size)]

    # Nombre de blocs (sans le IV)
    nb_blocks = len(cipher_blocks) - 1

    # Initialisation du résultat
    plain_text = bytearray()

    # Déchiffrement par blocs
    for i in range(nb_blocks):
        # Récupération des blocs
        current_block = cipher_blocks[-(i + 1)]
        previous_block = cipher_blocks[-(i + 2)]

        # Déchiffrement du bloc
        plain_block = decrypt_block(connection, current_block, previous_block)

        # Ajout du bloc en clair au texte entier
        plain_text = plain_block + plain_text
        print(plain_text)

    # Retour du texte en clair sans le padding
    return plain_text[:-plain_text[-1]].decode('utf-8')


def main() -> None:
    encrypted = bytes.fromhex(open("./cbc_ciphertext", "r").read().strip())
    connection = connect_to_oracle()

    plain = decrypt_via_padding_oracle(encrypted, connection)

    connection.close()
    print(plain)


if __name__ == "__main__":
    main()
