# Dialogue basé sur l'argumentation pour le choix d'un moteur de voiture

## Fonctionnement du git

### Fonctionnement du projet

### Organisation du git

#### Dossier arguments
Ce dossier contient la classe Argument ainsi que les différentes fonctions qui permettent de construire des arguments.
Le principe général est le suivant : 

Après que le deuxième agent est demandé d'expliquer le choix du premier on argumente avec un argument de type : mon critère préféré est GOOD ou VERY_GOOD.

Le deuxième agent contre-argumente en disant qu'un critère plus important est BAD ou VERY_BAD. S'il n'a aucun argument de ce type, il propose un autre moteur qu'il préfère pour lequel le critère dont il est question est meilleur ou égal. 

Le premier agent défend son moteur en contrant le contre-argument ou attaque le nouveau moteur. S'il ne peut pas attaquer le nouveau moteur car il n'a pas de contre-argument, il propose un nouveau moteur, meilleur à ses yeux. S'il n'a pas de nouveau moteur, il n'a pas d'autres choix que d'accepter.

#### Dossier communication
Ce dossier contient les dossiers agent, mailbox, message, motor et preferences. Le dossier motor contient une fonction permettant de générer une liste aléatoire de moteurs. Cette fonction permet donc de faire discuter nos agents sur un plus grand nombre de moteurs.
Sur les autres dossiers nous n'avons pas changé la structure.

#### Fichier pw_argumentation.py

### Résultats
Les résultats suivants sont pour un cas à 3 moteurs.

Cas où le moteur favori de l'agent 1 est dans les 10% préféré de l'agent 2 :  
![WhatsApp Image 2023-04-21 à 11 35 29](https://user-images.githubusercontent.com/82157628/233603790-84bc439b-997d-4082-a38b-a438cd446045.jpg)

Cas où on change de moteur une fois et on finit par l'accepter car on n'a pas de meilleure proposition : 
![Im3](https://user-images.githubusercontent.com/82157628/233605984-9c44a258-e98b-431f-8e68-d474b3723124.jpg)
