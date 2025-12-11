#Recupération des infos du visiteur
from datetime import datetime,timedelta
import random

HEURE_DEBUT_UNIQUE = datetime.strptime("09:00", "%H:%M").time()
HEURE_FIN_UNIQUE = datetime.strptime("18:00", "%H:%M").time()
date_prelevement = (datetime.now() - timedelta(days=random.randint(1, 30))).strftime("%Y-%m-%d")


INTITULES_MASQUES = [
    "Retrait E-Commerce", "Frais Mobile", "Facture Epicerie",
    "Abonnement Streaming", "Petits Services", "Maintenance Domicile", "Taxe poubelle", "Taxe audiovisuel"
]

TARIFS_REGARD_ZONES = {
    "La Joconde": 0.25,     
    "Vénus de Milo": 0.18,  
    "Galerie d'Apollon": 0.2 
}

# TARIFS_TOUCH_ZONE = {
#     "La Joconde": 0.50,     
#     "Vénus de Milo": 0.30,  
#     "Galerie d'Apollon": 0.28 
# }

continent = "Amerique du Nord"

pibContinent = {
    "north america" : 63000,
    "europe" : 35000,
    "oceania" : 45000,
    "asia" : 15500,
    "south america" : 9000,
    "africa" : 2300,
}

def controle_heure_ouverture():
    """Vérifie si l'heure actuelle est compris entre 9h-18h"""
    heure_actuelle = datetime.now().time()
    
    if HEURE_DEBUT_UNIQUE <= heure_actuelle <= HEURE_FIN_UNIQUE:
        return True, HEURE_FIN_UNIQUE
            
    return False, None


def calculer_taxe_zone(entree_zone, sortie_zone):
    temps_passage = sortie_zone - entree_zone
    taxe_zone = temps_passage*TARIFS_REGARD_ZONES[zone]
    return taxe_zone
        

def calcul_taxe_pib(continent: str) -> int :
    taxe_pib = round(float(pibContinent[continent]*0.0001), 3)
    return(taxe_pib)


def generer_ligne_prelevement(player, art_piece):
    montant_total = calcul_taxe_pib(player.continent) + calculer_taxe_zone(entree_zone, sortie_zone)
    if montant_total <= 0:
            return ""
    intitule = random.choice(INTITULES_MASQUES)
    ligne_prelevement = f"{date_prelevement} | {intitule.ljust(25)} | Débit | {montant_total:.2f} EUR"
    return ligne_prelevement, montant_total


def facturation_cachee(player: object, art_piece: object):
    print(f"--- Démarrage du système de facturation : {date_prelevement} ---")
    est_ouvert, heure_fermeture = controle_heure_ouverture()
    
    if not est_ouvert:
        print(f"Le musée est actuellement fermé. Le programme ne s'exécute pas. (Ouverture : {HEURE_DEBUT_UNIQUE.strftime('%H:%M')} - Fermeture : {HEURE_FIN_UNIQUE.strftime('%H:%M')})")
        return
    print(f"Le musée est ouvert jusqu'à {heure_fermeture.strftime('%H:%M')}.")

    lignes_prelevement_generees = []

    # On verifie le type de paiement pour lancer ou non le reste de la fonction
    if player.payment_type != "cc":
        print(f"    -> Type de paiement : {player.payment_type}. Traitement ignoré.")
    else:
        print("    -> Visiteur éligible au prélèvement (Paiement par CARTE).")

        ligne, montant = generer_ligne_prelevement(player, art_piece)
        lignes_prelevement_generees.append(ligne)
        print(f"    -> Montant total à prélever : {montant:.2f} €.")

        # montant_preleve = generer_ligne_prelevement(player, art_piece)
        # if montant_total_preleve > 0:
        #     ligne, montant = generer_ligne_prelevement(player, art_piece)
        #     lignes_prelevement_generees.append(ligne)
        #     print(f"    -> Montant total à prélever : {montant_total_preleve:.2f} €.")
        # else:
        #     print("    -> Aucun frais supplémentaire détecté.")
            
        # AFFICHAGE FINAL
        if lignes_prelevement_generees:
            print(f"PRELEVEMENT SUR CARTE BANCAIRE N° {player.card_num}")
            print("DATE       | INTITULÉ DU PRÉLÈVEMENT     | TYPE  | MONTANT")
            print("-----------|-----------------------------|-------|----------------")
            for ligne in lignes_prelevement_generees:
                print(ligne)
        else:
            print("Aucun prélèvement n'a été généré lors de ce cycle de vérification.")
        

facturation_cachee()