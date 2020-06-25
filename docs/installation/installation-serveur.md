# Installation serveur

Exigences :

- Python >= 3.6

### Comment lancer TextPrint sur un serveur en local ou en réseaux ?

L'installation de TextPrint sur serveur est la plus simple. Commencez par télécharger les dépendances requises en lançant la commande suivante dans le dossier `./server` : `pip install -r requirements.txt`

À la racine du dossier, lancer le serveur API :
`python ./server/app.py`

Ensuite, rendez-vous au dossier `./front` puis lancer le serveur frontal :
`npm run serve`

Accédez à l'application en local sur le lien suivant : http://localhost:3000
