import socket
import sys

from Crypto.Cipher import AES


def connect_to_server(server="51.195.253.124", port=11111) -> socket:
    soc_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc_con.connect((server, port))
    except Exception as e:
        print("Problème de connexion avec l'oracle", e.args)
        sys.exit(1)

    return soc_con


def is_valid_padding(soc: socket, cipher_block: str) -> bool:
    # Envoi des donnees
    soc.sendall(cipher_block.encode("utf-8"))

    # Enregistrement de la reponse
    ligne = soc.recv(1024)

    if ligne == b'Successfully decrypted.\n':
        return True

    return False


def decrypt_via_padding_oracle(cipher: bytes):
    # Découpage du texte chiffré en blocs
    cipher_blocks = [cipher[i * AES.block_size:(i + 1) * AES.block_size] for i in range(len(cipher) // AES.block_size)]
    # Initialisation du résultat
    plain = b""

    # Déchiffrement par blocs
    for i in range(len(cipher_blocks) - 1):
        plain_block = b""
        trail = b""

        connection = connect_to_server()

        # Attaque sur chaque octet du bloc
        for block_position in range(AES.block_size):
            # Test de chaque valeur possible
            for byte_value in range(256):
                cipher_block_attack = (15 - block_position) * b'\x00' + bytes([byte_value]) + trail
                cipher_both_block = b"".join([cipher_block_attack, cipher_blocks[-(i + 1)]])

                if is_valid_padding(connection, cipher_both_block.hex()):
                    last_plain = (block_position + 1) ^ cipher_blocks[-(i + 2)][15 - block_position] ^ byte_value
                    plain_block = bytearray([last_plain]) + plain_block
                    trail = b""

                    for k in range(block_position + 1):
                        last_byte = (block_position + 2) ^ plain_block[-k - 1] ^ cipher_blocks[-(i + 2)][15 - k]
                        trail = bytearray([last_byte]) + trail

                    break
        connection.close()
        plain = b"".join([plain_block, plain])
        print(plain)

    return plain[:-plain[-1]]


def main() -> None:
    encrypted = open("./cbc_ciphertext", "r").read().strip()
    plain = decrypt_via_padding_oracle(bytes.fromhex(encrypted))

    print(plain)


if __name__ == "__main__":
    main()
