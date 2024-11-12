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


def decrypt(cipher: bytes, mode=AES.MODE_CBC):
    cipher_blocks = [cipher[i * AES.block_size:(i + 1) * AES.block_size] for i in range(len(cipher) // AES.block_size)]
    res = b""
    for _ in range(len(cipher_blocks) - 1):
        plain = b""
        last_cipher_block = cipher_blocks[-1]
        trail = b""

        connection = connect_to_server()

        for i in range(AES.block_size):
            for j in range(256):
                flip = bytes([j])
                cipher_block_attack = (15 - i) * b'\x00' + flip + trail
                cipher_both_block = b"".join([cipher_block_attack, last_cipher_block])

                if is_valid_padding(connection, cipher_both_block.hex()):
                    print(cipher_both_block.hex())
                    last_plain = (i + 1) ^ cipher_blocks[-2][15 - i] ^ j
                    plain = bytearray([last_plain]) + plain
                    trail = b""

                    for k in range(i + 1):
                        last_byte = (i + 2) ^ plain[-k - 1] ^ cipher_blocks[-2][15 - k]
                        trail = bytearray([last_byte]) + trail

                    break

        connection.close()
        cipher_blocks = cipher_blocks[:-1]
        res = plain + res

    return res[:-res[-1]]


if __name__ == "__main__":
    # Le serveur nous donne l'information qu'il attend une cle de 16 octets (128 bits)
    encrypted = open("./cbc_ciphertext", "r").read().strip()
    plain = decrypt(bytes.fromhex(encrypted))

    print(plain)
