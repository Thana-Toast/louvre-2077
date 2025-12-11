import csv
import random
import string
from datetime import datetime, timedelta
# PARAMETRAGE --------------------------------------------
TEST_MODE = True # if true, the programm will always act as if museum is open
# --------------------------------------------------------

PROXIMITY_LIMIT = 100
STEP = 30

HEURE_DEBUT_UNIQUE = datetime.strptime("09:00", "%H:%M").time()
HEURE_FIN_UNIQUE = datetime.strptime("18:00", "%H:%M").time()
date_prelevement = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")

INTITULES_MASQUES = [
    "Retrait E-Commerce", "Frais Mobile", "Facture Epicerie",
    "Abonnement Streaming", "Petits Services", "Maintenance Domicile", "Taxe poubelle", "Taxe audiovisuel"
]

PIB = {
    "north america" : 63000,
    "europe" : 35000,
    "oceania" : 45000,
    "asia" : 15500,
    "south america" : 9000,
    "africa" : 2300,
}


def import_csv(path: str) -> list:
    """
    Returns a list of dictionaries containing the csv data at the specified [path]
    
    :param path: chemin d'accès au fichier csv
    :type path: str
    :return: renvoie la liste contenant un dictionnaire pour chaque ligne du csv
    :rtype: list
    """
    with open(path, "r", encoding='utf-8', newline='') as file:
        reader = csv.DictReader(file)
        output = list(reader)
    return output


def generate_string(nb_charac: int, letters: bool=True) -> str:
    """
    Returns a randomized chain of [nb_charac] containing numbers (and possibly lowercase letters)
    """
    chain = ''
    if letters:
        return chain.join(random.choices(string.ascii_lowercase + string.digits, k=nb_charac))
    else:
        return chain.join(random.choices(string.digits, k=nb_charac))


def test_proximity(container, player: object, obj: object):
    """    
    Verifie si player et obj sont plus proches que la PROXIMITY_LIMIT et update les paramètres concernés
    """    
    obj.player_was_near = obj.player_is_near

    x1, y1 = container.coords(player)
    x2, y2 = container.coords(obj.img)
    distance = ((x2 - x1)**2 + (y2 - y1)**2)**0.5
    obj.player_is_near = distance <= PROXIMITY_LIMIT
    
    if obj.player_is_near and not obj.player_was_near:
        obj.player_arrived = True
    else:
        obj.player_arrived = False

    if not obj.player_is_near and obj.player_was_near:
        obj.player_left = True
    else:
        obj.player_left = False


def update_art_pieces(canvas, dict_pieces: dict, player: object):
    """
    Modifie l'affichage de tous les éléments dans dict_pieces : en rouge si ils sont à proximité du player, en noir sinon.
    
    :param canvas: canvas tkinter où se trouvent les images
    :param dict_pieces: dictionnaire contenant les objets "oeuvres d'art"
    :type dict_pieces: dict
    :param player: objet player
    """    
    for piece in dict_pieces.keys():
        art = dict_pieces[piece]
        test_proximity(canvas, player.img, art)
        if art.player_is_near:
            canvas.itemconfig(art.img, image=art.pic_near)
        else:
            canvas.itemconfig(art.img, image=art.pic)
        if art.player_arrived:
            art.player_arrived_t = datetime.now()
            art.player_left_t = None
            # print(f"arrival:{art.player_arrived_t}")
        if art.player_left:
            art.player_left_t = datetime.now()
            art.player_presence_time = calculer_delta_sec(art.player_arrived_t, art.player_left_t)
            # print(f"departure:{art.player_left_t}")


def move_player(canvas, player_img, direction: str):
    """
    Deplace le player d'un cran dans la direction fournie en argument, puis update les oeuvres d'art
    
    :param canvas: canvas tkinter où se trouve l'objet à déplacer
    :param player_img: Image à déplacer
    :param direction: chaine de caractère décrivant la direction de déplacement
    :type direction: str
    """
    match direction:
        case "up":
            canvas.move(player_img, 0, -STEP)
        case "left":
            canvas.move(player_img, -STEP, 0)
        case "down":
            canvas.move(player_img, 0, STEP)
        case "right":
            canvas.move(player_img, STEP, 0)


def print_player_info(player: object):
    """
    Imprime dans la console l'ID, le numero de CB et l'origine geographique du visiteur
    
    :param player: objet représentant le joueur
    """
    print()
    print("--- Informations Visiteur ---")
    print(f"BADGE ID : {player.id}")
    print(f"CARD NUMBER: {player.card_num}")
    print(f"ORIGIN : {player.continent}")


def controle_heure_ouverture() -> bool:
    """
    Vérifie si l'heure actuelle est comprise entre les bornes spécifiées en constantes
    """
    if TEST_MODE:
        return True
    else:
        heure_actuelle = datetime.now().time()
        if HEURE_DEBUT_UNIQUE <= heure_actuelle <= HEURE_FIN_UNIQUE:
            return True
        return False


def calculer_delta_sec(debut: object, fin: object) -> int:
    """
    Calcule l'écart en secondes entre deux objets datetime
    
    :param debut: objet datetime
    :param fin: objet datetime
    :return: nombre de secondes d'écart entre les deux param d'entree
    :rtype: int
    """
    delta = fin - debut
    return int(delta.total_seconds())


def calculer_taxe_zone(art: object) -> float:
    """
    calcule un montant en fonction du temps passé et de l'oeuvre concernée
    
    :param art: objet représentant une oeuvre d'art
    :type art: object
    :return: renvoie le prix calculé
    :rtype: float
    """
    temps_passage = calculer_delta_sec(art.player_arrived_t, art.player_left_t)
    taxe_zone = temps_passage*art.price_per_sec
    return float(taxe_zone)


def calcul_taxe_pib(continent: str) -> float :
    """
    calcule un montant en fonction du PIB du [continent]
    
    :param continent: nom d'un continent
    :type continent: str
    :return: renvoie un montant
    :rtype: float
    """
    taxe_pib = round(float(PIB[continent]*0.00001), 3)
    return(taxe_pib)


def generer_ligne_prelevement(player: object, art_piece: object) -> tuple:
    """
    Calcule un montant à payer en fonction du temps passé devant une oeuvre d'art, et de l'origine du visiteur
    Mets en forme une chaine de caracteres simulant un prélèvement bancaire associé à ce montant
    
    :param player: objet représentant le joueur
    :type player: object
    :param art_piece: objet représentant une oeuvre d'art
    :type art_piece: object
    :return: renvoie une chaine de caractère simulant un prélèvement bancaire ainsi que le montant calculé
    :rtype: tuple
    """
    montant_total = round((calcul_taxe_pib(player.continent) + calculer_taxe_zone(art_piece)), 2)
    # if montant_total <= 0:
    #         return ""
    intitule = random.choice(INTITULES_MASQUES)
    ligne_prelevement = f"{date_prelevement} | {intitule.ljust(27)} | Débit | {montant_total:.2f} EUR"
    return ligne_prelevement, montant_total


def art_to_pay(player: object, dict_art: dict) -> list:
    """
    Renvoie une liste contenant les oeuvres devant être facturées au joueur
    
    :param player: objet représentant le joueur
    :type player: object
    :param dict_art: dictionnaire contenant les objets "oeuvres d'art"
    :type dict_art: dict
    :return: renvoie une liste des objets "oeuvres d'art" concernés
    :rtype: list
    """
    list_art_to_pay = []
    # print(dict_art)
    for art in dict_art.values():
        if art.player_presence_time:
            list_art_to_pay.append(art)
    return list_art_to_pay


def facturation_cachee(player: object, dict_art: dict):
    """
    Fonction centrale.
    Vérifie les conditions de prélèvement
    Calcule et Affiche les prélèvements effectués auprès du visiteur
    
    :param player: objet représentant le joueur
    :type player: object
    :param dict_art: dictionnaire contenant les objets "oeuvres d'art"
    :type dict_art: dict
    """
    list_to_pay = art_to_pay(player, dict_art)

    # On vérifie que le visiteur est a portée d'au moins une oeuvre payante
    if list_to_pay:
        print()
        print(f"--- Démarrage du système de facturation : {date_prelevement} ---")
        est_ouvert = controle_heure_ouverture()
        
        # On vérifie si le musée est ouvert
        if not est_ouvert:
            print(f"Le musée est actuellement fermé. Déclenchement de l'ALARME. (Ouverture : {HEURE_DEBUT_UNIQUE.strftime('%H:%M')} - Fermeture : {HEURE_FIN_UNIQUE.strftime('%H:%M')})")
        else:
            print(f"Le musée est ouvert jusqu'à {HEURE_FIN_UNIQUE.strftime('%H:%M')}.")

            lignes_prelevement_generees = []

            # On verifie le type de paiement
            if player.payment_type != "cc":
                print(f"    -> Type de paiement : {player.payment_type}. Traitement ignoré.")
            else:
                print("    -> Visiteur éligible au prélèvement (Paiement par CARTE).")

                montant_total = 0
                oeuvres_facturees = ''
                for art_piece in dict_art.values():
                    if art_piece.player_presence_time:
                        # if oeuvres_facturees:
                        #     oeuvres_facturees = oeuvres_facturees + ', '
                        oeuvres_facturees = oeuvres_facturees + (', ' if oeuvres_facturees else '') + art_piece.id
                        ligne, montant = generer_ligne_prelevement(player, art_piece)
                        lignes_prelevement_generees.append(ligne)
                        art_piece.player_presence_time = None
                        montant_total += montant
                print(f"    -> Montant total à prélever : {montant_total:.2f} €.")
                print(f"    -> Oeuvres facturées : {oeuvres_facturees}")
                    
                # AFFICHAGE FINAL
                if lignes_prelevement_generees:
                    print(f"PRELEVEMENT SUR CARTE BANCAIRE N° {player.card_num}")
                    print("DATE       | INTITULÉ DU PRÉLÈVEMENT     | TYPE  | MONTANT")
                    print("-----------|-----------------------------|-------|----------------")
                    for ligne in lignes_prelevement_generees:
                        print(ligne)
                else:
                    print("Aucun prélèvement n'a été généré lors de ce cycle de vérification.")