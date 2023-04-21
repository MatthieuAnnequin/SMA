# Dialogue basé sur l'argumentation pour le choix d'un moteur de voiture

### Le projet

### Introduction
Ce projet s'inscrit dans le cadre du cours de système multi-agent du parcours de 3A de CentraleSupélec, mention intelligence artificielle.

### Auteurs
- **Valentin Odde** - *AI master student* - [valentinodde](https://github.com/valentinodde)
- **Matthieu Annequin** - *AI master student* - [matthieuannequin](https://github.com/matthieuannequin)

## Fonctionnement du git
### Fonctionnement du projet

Pour exécuter le projet, nous vous invitons à cloner le répertoire avec l'instruction suivante : 
```sh
git clone https://github.com/MatthieuAnnequin/SMA.git
```

Pour lancer l'argumentation, nous vous invitons à vous reporter à la section pw_argumentation.

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

C’est le fichier d’execution de notre projet, c’est à cet endroit que l’on a créé notre classe **`ArgumentAgent`** qui hérite de  **`Communicating Agent`**. 
Il contient également la classe **`ArgumentModel`** qui hérite directement de  la classe **`Model`** de la bibliothèque *mesa*. 

Pour l'éxécuter, nous pouvons taper l'instruction suivante dans la console en nous plaçant dan le dossier **`SMA`** afin de lancer une argumentation entre nos 2 agents.
```sh
python -m pw_argumentation
```

Cela va exécuter le code suivant qui permet de lancer une simulation sur 20 étapes avec par défaut 3 moteurs différents, ce nombre peut être ajusté afin d'avoir un plus grand nombre de moteur.
```sh
def launch_step(n=20):
    print('Launch ArgumentModel')
    argument_model = ArgumentModel()
    step = 0
    while step < n:
        argument_model.step()
        step += 1
```

## Résultats
Les résultats suivants sont pour un cas à 3 moteurs.

Cas où le moteur favori de l'agent 1 est dans les 10% préféré de l'agent 2 :  
![WhatsApp Image 2023-04-21 à 11 35 29](https://user-images.githubusercontent.com/82157628/233603790-84bc439b-997d-4082-a38b-a438cd446045.jpg)

Cas où on change de moteur une fois et on finit par l'accepter car on n'a pas de meilleure proposition : 
![Im3](https://user-images.githubusercontent.com/82157628/233605984-9c44a258-e98b-431f-8e68-d474b3723124.jpg)
