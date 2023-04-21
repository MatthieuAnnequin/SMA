# Dialogue basé sur l'argumentation pour le choix d'un moteur de voiture

## Fonctionnement du git

### Fonctionnement du projet

### Organisation du git

#### Dossier arguments
Ce dossier contient la classe Argument ainsi que les différentes fonctions qui permettent de construire des arguments.

#### Dossier communication
Ce dossier contient les dossiers agent, mailbox, message, motor et preferences. Le dossier motor contient une fonction permettant de générer une liste aléatoire de moteurs. Cette fonction permet donc de faire discuter nos agents sur un plus grand nombre de moteurs.
Sur les autres dossiers nous n'avons pas changé la structure.

#### Fichier pw_argumentation.py

### Résultats
Les résultats suivants sont pour un cas à 3 moteurs.

Cas où le moteur favori de l'agent 1 est dans les 10% préféré de l'agent 2 :  
![WhatsApp Image 2023-04-21 à 11 35 29](https://user-images.githubusercontent.com/82157628/233603790-84bc439b-997d-4082-a38b-a438cd446045.jpg)

Cas où on change une fois de moteur dans la discussion :
![Im2](https://user-images.githubusercontent.com/82157628/233605313-e35ab3df-1f1a-4347-9b36-ba2c890bd801.jpg)

Cas où on change de moteur une fois et on finit par l'accepter car on n'a pas de meilleure proposition : 
![Im3](https://user-images.githubusercontent.com/82157628/233605984-9c44a258-e98b-431f-8e68-d474b3723124.jpg)
