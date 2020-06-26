# TextPrint (prototype fonctionnel)

Application de comparaison d'auteurs.

Exigences :

- Python == 3.6 (version 3.6 obligatoire)
- Node.JS == 11 (version 11 de préférence)
- MacOS ou Linux (pour Windows, il est nécessaire d'utiliser un outil tel que CMake car makefile n'est pas pris en charge nativement par cette plateforme, pour plus de simplicité, préférez une installation manuelle sous Windows)

## Installation et mise en place

Pour commencer , lancez à la racine de ce dossier la commande suivante qui installera les dépendances nécessaires :
`make install` (à lancer une seule fois, au lancement de cette commande, la base de données se réinitialise).

Une fois les dépendances installées, pour lancer l'application :
`make run`

Lien des processus :

- Plateforme Web : http://localhost:8080
- Plateforme API : http://localhost:5000
- Documentation interactive : http://localhost:3000
