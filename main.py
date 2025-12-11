import tkinter as tk
from functions_main import *
import random


# TO DO:
# - Calcul temps présence ?
# - Affichage console infos visiteur 

# CONSTANTES --------------------------------------------------------------------------------------------------
NB_COLUMNS = 15
HEIGHT_CANVAS = 500
WIDTH_CANVAS = 500
START_X = 250
START_Y = 500
LIST_CONTINENTS = ["africa", "asia", "europe", "north america", "oceania", "south america"]
# --------------------------------------------------------------------------------------------------------------


# CLASSES --------------------------------------------------------------------------------------------------
class Visitor:
    def __init__(self):
        # self.begin = True
        self.id = "000001"
        self.payment_type = "cc"
        self.card_num = None
        self.continent = "europe"
        self.pic = tk.PhotoImage(file="visiteur.png")
        self.img = None

class ArtPiece:
    def __init__(self):
        self.id = "art_piece"
        self.position = (0, 0)
        self.price_per_sec = 0.1
        self.player_is_near = False
        self.player_was_near = False
        self.player_arrived = False
        self.player_arrived_t = None
        self.player_left = False
        self.player_left_t = None
        self.player_presence_time = None
        self.pic = tk.PhotoImage(file="oeuvre.png")
        self.pic_near = tk.PhotoImage(file="oeuvre_active.png")
        self.img = None
# --------------------------------------------------------------------------------------------------------------

def button_action(canvas, player: object, dict_pieces: dict, move_direction: str):
    """
    Declenche toutes les actions lorsque l'utilisateur appuie sur un bouton:
    - déplacement
    - modification des propriétés des oeuvres d'art
    - déclenchement de la facturation
    
    :param canvas: canvas d'affichage
    :param player: objet représentant le joueur
    :type player: object
    :param dict_pieces: dictionnaire contenant les objets "oeuvres d'art"
    :type dict_pieces: dict
    :param move_direction: chaine décrivant la direction de déplacement
    :type move_direction: str
    """
    move_player(canvas, player.img, move_direction)
    update_art_pieces(canvas, dict_pieces, player)
    facturation_cachee(player, dict_pieces)


# MAIN -------------------------------------------------------------------------------------------------------
window = tk.Tk()

# Definition des images Buttons
up_pic = tk.PhotoImage(file="up.png")
left_pic = tk.PhotoImage(file="left.png")
down_pic = tk.PhotoImage(file="down.png")
right_pic = tk.PhotoImage(file="right.png")

# Config grille en 5 colonnes
for i in range(NB_COLUMNS):
    window.grid_columnconfigure(i, weight=1)

# Canevas
bg_img = tk.PhotoImage(file="bg.png")
canvas = tk.Canvas(window, width=WIDTH_CANVAS, height=HEIGHT_CANVAS, bg="white")
canvas.grid(row=0, column=0, columnspan=NB_COLUMNS, pady=10)
canvas.create_image(0, 0, anchor="nw", image=bg_img)

# Buttons
up = tk.Button(window, text = "Haut", command = lambda: (
    button_action(canvas, player, dict_pieces, "up")
), image = up_pic)
left = tk.Button(window, text = "Gauche", command = lambda: (
    button_action(canvas, player, dict_pieces, "left")
), image = left_pic)
down = tk.Button(window, text = "Bas", command = lambda: (
    button_action(canvas, player, dict_pieces, "down")
), image = down_pic)
right = tk.Button(window, text = "Droite", command = lambda: (
    button_action(canvas, player, dict_pieces, "right")
), image = right_pic)

central_column = (NB_COLUMNS//2)
up.grid(row=1, column=central_column, pady=5)
left.grid(row=2, column=central_column-1, pady=5)
down.grid(row=2, column=central_column, pady=5)
right.grid(row=2, column=central_column+1, pady=5)

# Initialisation player
player = Visitor()
player.id = generate_string(6)
player.card_num = generate_string(16, letters=False)
player.continent = LIST_CONTINENTS[random.randrange(len(LIST_CONTINENTS))]
player.img = canvas.create_image(START_X, START_Y, image=player.pic)
print_player_info(player)

# Initialisation des oeuvres
list_art = import_csv("art_pieces.csv")
dict_pieces = {}
for piece in list_art:
    dict_pieces[piece["id"]] = ArtPiece()
    dict_pieces[piece["id"]].id = piece["id"]
    dict_pieces[piece["id"]].position = (piece["x"], piece["y"])
    dict_pieces[piece["id"]].price_per_sec = float(piece["price_per_sec"])
    dict_pieces[piece["id"]].pic = tk.PhotoImage(file=piece["pic_file"])
    dict_pieces[piece["id"]].pic_near = tk.PhotoImage(file=piece["active_pic_file"])
    dict_pieces[piece["id"]].img = canvas.create_image(piece["x"], piece["y"], image=dict_pieces[piece["id"]].pic)

window.mainloop()
# --------------------------------------------------------------------------------------------------------------
