import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image

# Fonction pour lire les données depuis un fichier binaire
def lire_image_fichier(fichier):
    with open(fichier, "rb") as f:
        # Lire tout le contenu du fichier binaire
        data = np.frombuffer(f.read(), dtype=np.uint16)
    return data

def tronquer_image(image, max_height=65500):
    # Si la hauteur de l'image est supérieure à max_height, on la tronque
    if image.shape[0] > max_height:
        image = image[:max_height, :]  # Conserver uniquement les premières max_height lignes
    return image

def formater_image(data, largeur):
    # Calculer la hauteur nécessaire (en découpant l'array)
    hauteur = len(data) // largeur
    
    # Vérifier si la dernière ligne est partielle
    if len(data) % largeur != 0:
        # Découper l'array sans la dernière ligne complète
        data = data[:hauteur * largeur]
    
    # Créer l'image sous forme de liste de lignes
    image = []
    for i in range(hauteur):
        image.append(data[i * largeur : (i + 1) * largeur])
    
    # Convertir la liste en un array numpy 2D
    image = np.array(image)

    # Normaliser les données à 8 bits pour l'enregistrement
    image_normalisee = (image / 256).astype(np.uint8)
    
    return image_normalisee

# Fonction pour essayer de reconstruire l'image en utilisant différentes largeurs
def essayer_largeur(data, largeurs_possibles):
    data = data
    for largeur in largeurs_possibles:
        # Calculer la hauteur possible en divisant la longueur totale par la largeur
        image_normalisee = formater_image(data, largeur)
        
        # Sauvegarder l'image au format JPEG
        fichier_sortie = f"image_{largeur}x.jpg"
        
        # Supposons que 'image' est votre tableau numpy d'origine
        image_tronquee = tronquer_image(image_normalisee, 8000)
        
        # Convertir l'image en niveau de gris (16 bits à 8 bits pour le format JPEG)
        image_pil = Image.fromarray(image_tronquee)  # Créer une image PIL
        image_pil = image_pil.convert('L')  # Convertir en niveaux de gris
        
        # Sauvegarder l'image en format JPEG
        image_pil.save(fichier_sortie, 'JPEG')
            
        print(f"Image sauvegardée dans le fichier {fichier_sortie}")
            
    print("Aucune largeur correcte trouvée.")
    return None

# Fonction principale
def main():
    fichier = 'le-calme-avant-la-tempest.bin'
    
    if not os.path.exists(fichier):
        print("Le fichier n'existe pas.")
        return

    # Lire les données du fichier
    data = lire_image_fichier(fichier)
    
    # Essayer plusieurs largeurs possibles (par exemple, 256, 512, 1024)
    largeurs_possibles = range(1006, 2000, 2)
    largeurs_possibles = [1780]
    
    # Essayer de reconstruire l'image
    image = essayer_largeur(data, largeurs_possibles)
    
    if image is not None:
        print("Image trouvée et affichée avec succès.")
    else:
        print("Impossible de trouver une largeur correcte pour l'image.")

if __name__ == "__main__":
    main()



# FCSC{T3MP3ST_F0R3V3R}