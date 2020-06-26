# Installation serveur

Exigences :

- Python == 3.6
- Node.JS == 11 (de préférence)

### Comment installer de manière automatisée l'application TextPrint ?

⚠️ **En cas d'erreur lors de l'installation automatisée, préférez l'installation manuelle (voir ci-dessous)**

Pour commencer, lancez à la racine du dossier source de l'application la commande suivante qui installera les dépendances nécessaires :
`make install` (à lancer une seule fois, au lancement de cette commande, la base de données se réinitialise).

Une fois les dépendances installées, pour lancer l'application :
`make run`

Lien des processus en cours au lancement :

- Plateforme Web : http://localhost:8080
- Plateforme API : http://localhost:5000
- Documentation interactive : http://localhost:3000

### Comment installer manuellement TextPrint sur un serveur en local ou en réseaux ?

L'installation de TextPrint sur serveur est la plus simple. Commencez par télécharger les dépendances requises en lançant la commande suivante dans le dossier `./server` : `pip install -r requirements.txt`

À la racine du dossier, lancer le serveur API :
`python ./server/app.py`

Ensuite, rendez-vous au dossier `./front` puis lancer le serveur frontal :
`npm run serve`

Accédez à l'application en local sur le lien suivant : http://localhost:8080
