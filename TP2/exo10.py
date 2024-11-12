import string
import sys, socket, csv, time
from simple_term_menu import TerminalMenu
from colorama import init, Fore, Style

init()

def await_input() -> None:
    """
    Fonction permettant d'attendre une saisie utilisateur pour continuer
    :return: None
    """

    input("Appuyez sur Entrée pour continuer...")


def connect_to_server(server="51.195.253.124", port=22222) -> socket:
    soc_con = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        soc_con.connect((server, port))
    except Exception as e:
        print("Problème de connexion avec l'oracle", e.args)
        sys.exit(1)

    return soc_con

def find_length_of_password(ma_socket: socket.socket, expected_message: string) -> int:
    """
    Fonction permettant de retourner la taille du mot de passe utilisé pour le serveur
    :param ma_socket: Socket utilisateur permettant de se connecter au site internet
    :return: retourne un entier qui sera la taille du mot de passe.
    """
    arbitrary_string = "a"
    ma_socket.sendall(bytes(arbitrary_string.zfill(4), 'utf-8'))
    ligne = str(ma_socket.recv(1024))

    # Dans le cas ou le mot de passe est de longueur 1
    if ligne == expected_message:
        return len(arbitrary_string)

    # Tant qu'on a pas le message attendu pour dire qu'on a la bonne taille alors on augmente la chaine de caractère
    while ligne != expected_message:
        arbitrary_string += "a"
        ma_socket.sendall(bytes(arbitrary_string.zfill(4), 'utf-8'))
        ligne = str(ma_socket.recv(1024))

    return len(arbitrary_string)

def find_pin_without_optimisation(ma_socket: socket.socket, password_length: int) -> None:
    """
    Fonction permettant de se connecter au site internet
    :param ma_socket: Socket utilisateur permettant de se connecter au site internet
    :param password_length: Taille du mot de passe
    :return: None
    """
    password_use = ""
    password_found = False
    caracters = ["a"] * password_length
    print('Recherche du mot de passe...')
    caracteres_ascii = string.printable
    incorrect_message = repr(b'Bad password\n')

    for position in range(password_length):
        timers = []
        for caracter in caracteres_ascii:
            sample_times = []
            for _ in range(8):
                timer_start = time.time()
                ma_socket.sendall(bytes(caracter, 'utf-8'))
                ma_socket.recv(1024)
                timer_end = time.time()
                sample_times.append(timer_end - timer_start)

            avg_time = sum(sample_times) / len(sample_times)
            timers.append((caracter, avg_time))

        caractere_max = max(timers, key=lambda x: x[1])[0]
        print(f"Caractère{position}: {caractere_max}")
        caracters[position] = caractere_max

    caracters = ''.join(caracters)
    print("La proposition que nous testons est : ", caracters)

    ma_socket.sendall(bytes(str(caracters), 'utf-8'))
    ligne = str(ma_socket.recv(1024))
    print(ligne)
    if not ligne == incorrect_message and len(ligne) == password_length:
        password_use = caracters
        password_found = True

    if password_found:
        print(Fore.GREEN, "Password found")
        print("Le mot de passe utilisé est : ", password_use)
        return
    else:
        print(Fore.RED, "Suite non concluante !")
        print(Fore.RED, "On va appliquer à nouveau l'algorithme !")
        print(Style.RESET_ALL)
        find_pin_without_optimisation(ma_socket, password_length)




def restart_socket(ma_socket:socket.socket, server: str, port: int) -> socket.socket:
    """
    Fonction permettant de renouveller la socket. Si nous voulons tester les deux méthodes sans quitter le programme il
    faut nécessairement passer par cette méthode.
    :param ma_socket: Socket utilisateur permettant de se connecter au site internet
    :return: la socket renouvellée
    """
    ma_socket.close()
    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        sys.exit(1)

    ma_socket.recv(1024)

    return ma_socket


if __name__ == "__main__":
    main_title = "Authentification à un site\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Méthode sans trier les codes possibles", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)
    connection = connect_to_server()


    while True:
        main_entry_index = main_menu.show()
        if main_entry_index == 0:
            expected_message = repr(b'Bad password\n')
            password_length = find_length_of_password(connection, expected_message)
            find_pin_without_optimisation(connection, password_length)
            await_input()
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)