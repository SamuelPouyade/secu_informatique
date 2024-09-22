import string
import collections
import re
from simple_term_menu import TerminalMenu

def vigenere_cipher_input(encrypt=True) -> None:
    """
    Fonction permettant la saisie utilisateur d'un message dans le terminal et procède au chiffrement ou déchiffrement
    du message à l'aide du chiffrement de Vigenère
    :param encrypt: chiffrement (True par défaut) ou déchiffrement (False)
    :return: Le message chiffré ou déchiffré dans le terminal
    """

    input_text = ""

    # Le message ne doit pas être vide
    while input_text == "":
        input_text = input(f"Entrez le message à {"chiffrer" if encrypt else "déchiffrer"} : ")

    # Le décalage doit être un nombre entier positif
    while True:
        try:
            input_offset = (input("Saisissez la clé de chiffrement : "))
            if len(input_offset) <= 0:
                print("Veuillez saisir la clé de chiffrement")
                continue
            break
        except ValueError:
            print("Erreur lors de la saisie de la clé")

    if encrypt:
        message = vigenere_cipher(input_text, input_offset)
        print('Le message chiffré est: ', message)
    else:
        message = vigenere_decipher(input_text, input_offset)
        print('Le message déchiffré est: ', message)

def kasiski_input():
    """
    Fonction permettant la saisie utilisateur d'un message dans le terminal et d'effectuer le test de Kasiski
    :return: La liste des possibilité de longueur de clé
    """

    input_text = ""

    # Le message ne doit pas être vide
    while input_text == "":
        input_text = input("Entrez le message à analyser : ")

    all_position = findAllRepetitions(input_text)
    refineMultiple(all_position)

def cryptanalyse_input():
    """
    Fonction permettant la saisie utilisateur d'un message dans le terminal et d'effectuer une cryptanalyse
    :return: La liste des possibilité de longueur de clé
    """

    input_text = ""

    # Le message ne doit pas être vide
    while input_text == "":
        input_text = input("Entrez le message à cryptanalyser : ")

    all_tab_to_analyse = divide_text(input_text)

    for i in range(len(all_tab_to_analyse)):
        find_key(all_tab_to_analyse[i])



def convert_letter_to_number(text: string):
    """
    :param text: the message to be encrypted
    :return: the encrypted message
    """

    upper_text = text.upper()
    positions = []

    for char in upper_text:
        alphabet_position = ord(char) - ord('A')
        positions.append(alphabet_position)

    return positions


def vigenere_cipher(message: string, encryption_key: string):
    message = convert_letter_to_number(message)

    position_of_letter_of_encryption_key = convert_letter_to_number(encryption_key)

    if len(message) > len(position_of_letter_of_encryption_key):
        multiplicator = (len(message) // len(position_of_letter_of_encryption_key)) + 1
        encryption_key = position_of_letter_of_encryption_key * multiplicator


    counter = 0
    final_position = []
    cypher_message = []

    for position in message:
        if position < 0 or position > 25:
            final_position.append(position)
        else:
            final_position.append((position + encryption_key[counter]) % 26)
            counter += 1

    for position in final_position:
        cypher_message.append(chr(ord('A') + position))

    return ''.join(cypher_message)


def vigenere_decipher(message: string, decipher_key: string):
    message = convert_letter_to_number(message)
    position_of_letter_of_encryption_key = convert_letter_to_number(decipher_key)

    if len(message) > len(position_of_letter_of_encryption_key):
        multiplicator = (len(message) // len(position_of_letter_of_encryption_key)) + 1
        decipher_key = position_of_letter_of_encryption_key * multiplicator

    counter = 0
    final_position = []
    decipher_message = []

    for position in message:
        print(decipher_key[counter])
        if position < 0 or position > 25:
            final_position.append(position)
        else:
            final_position.append((position - decipher_key[counter]) % 26)
            counter += 1

    for position in final_position:
        decipher_message.append(chr(ord('A') + position))

    return ''.join(decipher_message)

def get_all_multiple (number: int) -> [int]:
    '''
    Fonction permettant d'avoir tout les multiples d'un nombre
    :param number: Le nombre à analyser
    :return: L'ensemble des multiples et le nombre analysé
    '''
    half_number = number // 2
    all_multiple = []
    all_multiple.append(number)

    # On ajoute un car la boucle for exclu la valeur N
    for i in range(2, half_number + 1):
        if number % i == 0:
            all_multiple.append(i)

    return all_multiple


def findAllRepetitions (text: string) :
    '''
    Fonction permettant de trouver toutes les répétitions possibles sans effectuer de tri
    :param text: Le texte à analyser
    :param possible_length: Objet stockant toutes les tailles possibles
    :return: Un objet contenant toutes les tailles possibles associés aux mots répétés
    '''
    possible_length = {}
    length = len(text)
    start_number = 0
    last_start_number = 0
    end_number = 2
    last_word = ''
    text = re.sub(r'[^A-Za-z]', '', text)

    while start_number < (length // 2) :
        if end_number < length // 2:
            end_number += 1

        if end_number > length // 2:
            break

        elif end_number == length // 2 :
            if start_number < length // 2:
                last_start_number += 1
                start_number = last_start_number + 1
                end_number = start_number + 2

        suite = text[start_number:end_number]

        # Si la chaine contient un espace nous l'ignorons.
        if ' ' in suite:
            continue

        if suite == last_word:
            continue

        nombre_rep = text.count(suite)

        if nombre_rep <= 1:
            start_number += 1
            continue
        else:
            all_occurence = []
            all_difference = []
            last_occurence = 0

            # Permet d'obtenir toutes les positions à laquelle la suite de lettre est répétée
            for i in range(nombre_rep):
                position = text.find(suite, last_occurence)
                all_occurence.append(position)
                # On augmente de 1 juste pour avoir un décalage et trouver la seconde position.
                last_occurence = position + len(suite)

            for i in range(len(all_occurence) - 1):
                if all_occurence[i] == 0 :
                    all_difference.append(all_occurence[i + 1])
                else:
                    all_difference.append(all_occurence[i+1] - all_occurence[i])

            # Le décalage n'est pas identique partout, il ne faut pas pousser les valeurs.
            if len(set(all_difference)) != 1:
                start_number += 1
                continue

            all_multiples = get_all_multiple(all_difference[0])
            possible_length[suite] = all_multiples

            possible_length = delete_useless_data(suite, possible_length)

            start_number += 1

    return possible_length

def delete_useless_data(suite, possible_length):
    '''
    Fonction permettant de supprimer des valeurs inutiles
    :param suite: La suite de caractères
    :param possible_length: Le tableau contenant les différentes tailles possibles
    :return: Retourne le tableau sans doublon
    '''

    data_to_delete = []
    for property in possible_length:
        if property != suite and len(property) != len(suite):
            if property.startswith(suite) or suite.startswith(property) or suite.endswith(property) or property.endswith(suite):
                if len(property) > len(suite):
                    data_to_delete.append(suite)
                else:
                    data_to_delete.append(property)

    for property in data_to_delete:
        if property in possible_length:
            del possible_length[property]

    return possible_length


def refineMultiple (all_repetitions) :
    '''
    Fonction permettant d'affiner les choix selectionnables par l'utilisateur
    :param all_repetitions: L'objet contenant toutes les répétitions
    :return: Retourne l'ensemble des tailles possibles
    '''
    print('Voici pour chaque suite les multiples pouvant définir la taille de la clé: ', object)
    print('Un second traitement arrive pour afiner les résultats...')

    if len(all_repetitions) == 0:
        print('Aucune suite ne se répète, nous ne pouvons pas trouver la longueur de la clé')
        return []
    elif len(all_repetitions) == 1:
        first_key = list(all_repetitions.keys())[0]
        print('Les possibilités sont: ', all_repetitions[first_key])
        return all_repetitions[first_key]
    elif len(all_repetitions) > 1:
        all_values = []
        for property in all_repetitions:
            for value in all_repetitions[property]:
                all_values.append(value)

        most_frequent_multiple = collections.Counter(all_values).most_common()[0][1]
        if most_frequent_multiple != len(all_repetitions):
            print('Aucun multiple est présent pour chacunes des chaines se répétant')
            most_frequent_multiple = collections.Counter(all_values).most_common(int(len(set(all_values)) * 0.10))
            multiple_without_repetitions = []
            if most_frequent_multiple:
                for element in most_frequent_multiple:
                    multiple_without_repetitions.append(element[0])
            else:
                for element in all_values:
                    multiple_without_repetitions.append(element)
            print('Les multiples qui apparaissent 10% de fois plus que les autres sont : ', multiple_without_repetitions)
            return multiple_without_repetitions
        else:
            most_frequent_multiple = collections.Counter(all_values).most_common()[0][0]
            print(collections.Counter(all_values).most_common())
            print('La clé est de la taille : ', most_frequent_multiple)
            return most_frequent_multiple

def divide_text (text: string) -> list:
    """
    Permet de séparer le texte par la longueur de la clé possible
    :param text: Le texte chiffré
    :return: Retourne un tableau contenant le texte séparé en plusieurs longueurs
    """
    all_position = findAllRepetitions(text)
    all_length = refineMultiple(all_position)
    text_without_space = text.replace(' ', '')
    all_separates_tab = []

    if len(all_length) != 0 or all_length != 0:
        for length in all_length:
            redefined_table = [''] * length
            for position, char in enumerate(text_without_space):
                redefined_table[position % length] += char
            # print('Pour un tableau de taille: ', length, ' Le texte redéfini se sépare tel quel: ', redefined_table)
            all_separates_tab.append(redefined_table)

    return all_separates_tab

def find_key(all_character_string_to_analyse)-> None:
    """
    Fonction permettant de trouver toutes les clés possibles en fonction de chaines de caractères
    :param all_character_string_to_analyse: Un tableau contenant toutes les chaines de caractères à analyser
    """
    length_of_key = len(all_character_string_to_analyse)
    all_possible_keys = []
    all_possible_caracteres = ['E', 'A', 'I', 'S', 'T']
    character_to_be_analysed = {}
    all_word = []

    get_all_max_repetitions(all_character_string_to_analyse, character_to_be_analysed)

    build_word(0, '', all_word, character_to_be_analysed)

    for possible_charactere in all_possible_caracteres:
        for word in all_word:
            key = ''
            for character in word:
                position = ord(character) - ord(possible_charactere)
                key += chr(ord('A') + (position % 26))
            all_possible_keys.append(key)

    print(f"Pour une clé de longueur : \"{length_of_key}\" nous obtenons la clé suivante: ", all_possible_keys)


def get_all_max_repetitions(all_character_string_to_analyse, character_to_be_analysed):
    """
    Fonction permettant de trouver toutes les lettres qui se répètent le plus. Tout en prenant en compte que plusieurs lettres ont le même nombre de répétitions
    :param all_character_string_to_analyse: Ensemble de chaine de caractères à analyser
    :param character_to_be_analysed: Tableau qui contiendra les caractères à analyser après cette fonction
    :return:
    """
    position = 0
    for element in all_character_string_to_analyse:
        character_of_element = []
        all_repetitions = collections.Counter(element)
        max_repetition = collections.Counter(element).most_common(1)[0][1]
        for character in element:
            if (ord(character) - ord('A')) < 0 or (ord(character) - ord('A')) > 25:
                continue
            else:
                if all_repetitions[character] == max_repetition and character not in character_of_element:
                    character_of_element.append(character)
        character_to_be_analysed[position] = character_of_element
        position += 1


def build_word(actual_position: int, partial_word, all_word, all_position_with_letter) :
    if actual_position == len(all_position_with_letter):
        all_word.append(partial_word)
        return

    for letter in all_position_with_letter[actual_position]:
        word = partial_word + letter

        build_word(actual_position + 1, word, all_word, all_position_with_letter)


def await_input() -> None:
    """
    Fonction permettant d'attendre une saisie utilisateur pour continuer
    :return: None
    """

    input("Appuyez sur Entrée pour continuer...")

if __name__ == "__main__":
    main_title = "Chiffrement de Vigenère\nAppuyez sur les flèches pour naviguer et sur Entrée pour sélectionner"
    main_options = ["Chiffrement", "Déchiffrement", 'Test de kasiski', 'Cryptanalyse', None, "Quitter"]
    main_menu = TerminalMenu(main_options, title=main_title, cycle_cursor=True, clear_screen=True)

    while True:
        main_entry_index = main_menu.show()
        # Chiffrement
        if main_entry_index == 0:
            vigenere_cipher_input(True)
            await_input()
        # Déchiffrement
        elif main_entry_index == 1:
            vigenere_cipher_input(False)
            await_input()
        # Test de Kasiski
        elif main_entry_index == 2:
            kasiski_input()
            await_input()
        # Cryptanalyse
        elif main_entry_index == 3:
            cryptanalyse_input()
            await_input()
        # Quitter
        elif main_entry_index == len(main_options) - 1 or main_entry_index is None:
            print("Au revoir !")
            exit(0)

