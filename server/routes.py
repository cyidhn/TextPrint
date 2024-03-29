#
# TextPrint
# Laboratoire IDHN
#

#
# Importations
#
from flask import render_template
from flask import request, make_response, redirect, session, escape
from app import app
from db import db_add, db_init, db_search
from flask import jsonify
import json
import os.path
import calendar
import time
from analyse import *
from classification import *
from lemmatisation import *
from bag_of_words import *
from reinert import *
from ngrammes import analyse_ngrammes_mots, analyse_ngrammes_chars, analyse_ngrammes_pos
from analyse_idhn import *
from langdetect import detect
import chardet
import io
import sys
# For IDHN
from zipfile import *

#
# Route de base
#
@app.route('/')
def index():
    db_init()
    if 'connect' in session:
        if session['connect'] == 1:
            return redirect('/page')
    return render_template('index.html')


@app.route('/page')
def page():
    if 'connect' in session:
        if session['connect'] == 1:
            return render_template('page.html')
    return redirect('/')


@app.route('/deconnexion')
def deconnexion():
    session['connect'] = 0
    return redirect('/')


@app.route('/connexion')
def connexion():
    session['connect'] = 1
    return redirect('/page')

#
# Route dynamique
#

#
# Code pour IDHN
# A supprimer en prod!!!
#
#
# ZIP file
#
@app.route("/importer-image-idhn", methods=["POST"])
def importerImg():
    if request.method == 'POST':

        # Ajout du fichier
        path = 'static/idhn_image'
        ts = calendar.timegm(time.gmtime())
        f = request.files['import']
        name = str(ts) + ".txt"
        name_return = str(ts)
        fa = os.path.join(path, name)
        f.save(fa)
        content = open(fa, "rb").read()
        result = chardet.detect(content)
        if (result['encoding'] != "utf-8"):
            if (result['encoding'] == "ISO-8859-1"):
                content = content.decode('iso-8859-1').encode('utf8')
                # return "Le fichier doit être en UTF-8", 405
            elif (result['encoding'] == "UTF-8-SIG"):
                print("Alright")
                # return "Fichier conforme", 200
            else:
                return "Le fichier doit être codé en UTF-8", 405
        content = content.decode('utf8')
        fi = open(fa, "w")
        fi.write(content)
        fi.close()

        # Premieres analyses
        # analyse_global_idhn(fa, "1", "1")

        # Detecter langue
        content = open(fa, "r")
        texte = content.read()
        content.close()
        langue = detect(texte)

        # Affichage langue
        if (langue == 'fr'):
            langue = "Français"
        elif (langue == 'es'):
            langue = "Espagnol"
        elif (langue == 'en'):
            langue = "Anglais"
        else:
            langue = "Non spécifiée"

        # Return
        return jsonify(
            langue=langue,
            name=name_return
        )
        # return name_return, 201

    # return "Problem"


@app.route('/download-idhn/<elementId>')
def downloadIdhn(elementId):
    path = 'static/textes'
    myZip = os.path.join(path, elementId + '.zip')
    # create a ZipFile object
    zipObj = ZipFile(myZip, 'w')

    # Add multiple files to the zip
    zipObj.write(os.path.join(path, elementId + '.txt'))
    zipObj.write(os.path.join(path, elementId + '_analyse.html'))

    # close the Zip File
    zipObj.close()
    return redirect('/static/textes/' + elementId + '.zip')


@app.route("/importer-texte-idhn", methods=["POST"])
def importerTexteIdhn():
    if request.method == 'POST':

        # Ajout du fichier
        path = 'static/idhn'
        ts = calendar.timegm(time.gmtime())
        f = request.files['importer-texte']
        name = str(ts) + ".txt"
        name_return = str(ts)
        fa = os.path.join(path, name)
        f.save(fa)
        content = open(fa, "rb").read()
        result = chardet.detect(content)
        if (result['encoding'] != "utf-8"):
            if (result['encoding'] == "ISO-8859-1"):
                content = content.decode('iso-8859-1').encode('utf8')
                # return "Le fichier doit être en UTF-8", 405
            elif (result['encoding'] == "UTF-8-SIG"):
                print("Alright")
                # return "Fichier conforme", 200
            else:
                return "Le fichier doit être codé en UTF-8", 405
        content = content.decode('utf8')
        fi = open(fa, "w")
        fi.write(content)
        fi.close()

        # Premieres analyses
        analyse_global_idhn(fa, "1", "1")

        # Detecter langue
        content = open(fa, "r")
        texte = content.read()
        content.close()
        langue = detect(texte)

        # Affichage langue
        if (langue == 'fr'):
            langue = "Français"
        elif (langue == 'es'):
            langue = "Espagnol"
        elif (langue == 'en'):
            langue = "Anglais"
        else:
            langue = "Non spécifiée"

        # Return
        return jsonify(
            langue=langue,
            name=name_return
        )
        # return name_return, 201

    # return "Problem"


#
# Impression avec template
#
@app.route('/imprimer-collection/<elementId>')
def imprimerCollection(elementId):

    # Declaration variables
    statsTextes = ""
    statsProfils = ""
    statsCollections = ""
    titre = ""

    # Echapper element
    elementId = escape(elementId)

    # Requete de donnees
    req = "SELECT * FROM tpCollections WHERE id = %s" % (elementId)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Lire le titre du dossier
    for r in data:
        titre = r[1]

    # Requete de donnees
    req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s'" % (
        elementId, 'Collection')

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage des infos
    for r in data:
        if r[1] == "Collection" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsProfils += """
                <tr>
                    <th scope="row">Profil %s</th>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
                """ % (t[9], t[1], t[2] + " " + nom)
        if r[1] == "Collection" and r[2] == "Dossier":
            req = "SELECT * FROM tpDossiers WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[1])
                statsCollections += """
                <tr>
                    <th scope="row">%s</th>
                    <td>-</td>
                    <td>-</td>
                </tr>
                """ % (titre)
        if r[1] == "Collection" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[2])
                statsTextes += """
                <tr>
                    <th scope="row">%s</th>
                    <td>1</td>
                </tr>
                """ % (t[2])

    return render_template('impression2.html', titre=titre, statsTextes=statsTextes, statsProfils=statsProfils, statsCollections=statsCollections)


@app.route('/imprimer-dossier/<elementId>')
def imprimerDossier(elementId):

    # Declaration variables
    statsTextes = ""
    statsProfils = ""
    statsCollections = ""
    titre = ""

    # Echapper element
    elementId = escape(elementId)

    # Requete de donnees
    req = "SELECT * FROM tpDossiers WHERE id = %s" % (elementId)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Lire le titre du dossier
    for r in data:
        titre = r[1]

    # Requete de donnees
    req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s'" % (
        elementId, 'Dossier')

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage des infos
    for r in data:
        if r[1] == "Dossier" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsProfils += """
                <tr>
                    <th scope="row">Profil %s</th>
                    <td>%s</td>
                    <td>%s</td>
                </tr>
                """ % (t[9], t[1], t[2] + " " + nom)
        if r[1] == "Dossier" and r[2] == "Collection":
            req = "SELECT * FROM tpCollections WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[1])
                statsCollections += """
                <tr>
                    <th scope="row">%s</th>
                    <td>-</td>
                    <td>-</td>
                </tr>
                """ % (titre)
        if r[1] == "Dossier" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[2])
                statsTextes += """
                <tr>
                    <th scope="row">%s</th>
                    <td>1</td>
                </tr>
                """ % (t[2])

    return render_template('impression.html', titre=titre, statsTextes=statsTextes, statsProfils=statsProfils, statsCollections=statsCollections)


#
# Autre
#
@app.route("/ngrams-pos-generate", methods=["POST"])
def ngramPos():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])
    mots = escape(request.form["mots"])
    mots = int(mots)

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = analyse_ngrammes_pos(fichier, n_grammes=mots, n_version=3)
        # Ajout en BD
        req = "INSERT INTO tpVersions (pretraitement, specification, idText, linkPretraitement) VALUES ('%s', '%s', %s,'%s')" % (
            "N-grammes de catégories grammaticales", str(mots) + " (nombre de N)", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/analyse-classification", methods=["POST"])
def analyseClassification():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = result_classification(
            chemin=fichier, model="./models/model_twitter.h5")
        # Affichage
        return fichier, 201
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/traitement-bow", methods=["POST"])
def traitementBow():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = traitement_bagofwords(fichier)
        # Ajout en BD
        req = "INSERT INTO tpVersions (pretraitement, specification, idText, linkPretraitement) VALUES ('%s', '%s', %s,'%s')" % (
            "Bag of Words", "", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/analyse-reinert", methods=["POST"])
def analysereinert():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = analyse_reinert(fichier)
        # Ajout en BD
        req = "INSERT INTO tpAnalyses (analyse, specification, idText, linkAnalyse) VALUES ('%s', '%s', %s,'%s')" % (
            "Analyse Reinert", "4 arbres générés", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "L'analyse a bien été créée", 201


@app.route("/ngrams-mots-generate", methods=["POST"])
def ngramMots():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])
    mots = escape(request.form["mots"])
    mots = int(mots)

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = analyse_ngrammes_mots(fichier, n_grammes=mots, n_version=2)
        # Ajout en BD
        req = "INSERT INTO tpVersions (pretraitement, specification, idText, linkPretraitement) VALUES ('%s', '%s', %s,'%s')" % (
            "N-grammes de mots", str(mots) + " (nombre de N)", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/traitement-lemmatisation", methods=["POST"])
def traitementLemmatisation():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = traitement_lemmatisation(fichier)
        # Ajout en BD
        req = "INSERT INTO tpVersions (pretraitement, specification, idText, linkPretraitement) VALUES ('%s', '%s', %s,'%s')" % (
            "Lemmatisation", "Lemmatisation du texte", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/ngrams-chars-generate", methods=["POST"])
def ngramChars():

    # Recuperer les donnees
    idTexte = escape(request.form["id"])
    fichier = escape(request.form["fichier"])
    mots = escape(request.form["mots"])
    mots = int(mots)

    # Convertir en lien de fichier
    fichier = "./static/textes/" + fichier + ".txt"

    # Executer
    try:
        print("Analyse en cours...")
        fichier = analyse_ngrammes_chars(fichier, n_grammes=mots, n_version=3)
        # Ajout en BD
        req = "INSERT INTO tpVersions (pretraitement, specification, idText, linkPretraitement) VALUES ('%s', '%s', %s,'%s')" % (
            "N-grammes de caractères", str(mots) + " (nombre de N)", idTexte, fichier)
        db_add(req)
    except:
        return "Erreur survenue...", 500

    # Renvoie resultat
    return "Le pré-traitement a bien été crée", 201


@app.route("/lastid-profil", methods=["GET"])
def lastidprofil():

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils ORDER BY id DESC LIMIT 1")

    # Boucle
    result = '[]'
    for r in req:
        result = '[{"id": %s}]' % (r[0])

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/lastid-dossier", methods=["GET"])
def lastiddossier():

    # Recherche en DB
    req = db_search("SELECT * FROM tpDossiers ORDER BY id DESC LIMIT 1")

    # Boucle
    result = '[]'
    for r in req:
        result = '[{"id": %s}]' % (r[0])

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/lastid-collection", methods=["GET"])
def lastidcollection():

    # Recherche en DB
    req = db_search("SELECT * FROM tpCollections ORDER BY id DESC LIMIT 1")

    # Boucle
    result = '[]'
    for r in req:
        result = '[{"id": %s}]' % (r[0])

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/lastid-texte", methods=["GET"])
def lastidtexte():

    # Recherche en DB
    req = db_search("SELECT * FROM tpTexte ORDER BY id DESC LIMIT 1")

    # Boucle
    result = '[]'
    for r in req:
        result = '[{"id": %s}]' % (r[0])

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/creer-dossier", methods=["POST"])
def creerDossier():

    # Recuperer les donnees
    titre = escape(request.form["titre"])

    # Verifier si le titre existe deja
    req = db_search("""SELECT * FROM tpDossiers WHERE titre='%s'""" % (titre))

    for r in req:
        return "Le titre attribué existe déjà. Merci de changer le nom du dossier.", 401

    # Requete pour inserer les donnees
    req = "INSERT INTO tpDossiers (titre) VALUES ('%s')" % (titre)

    # Inserer en bdd
    db_add(req)

    # Renvoie resultat
    return "Le dossier a bien été crée", 201


@app.route("/creer-collection", methods=["POST"])
def creerCollection():

    # Recuperer les donneesz
    titre = escape(request.form["titre"])

    # Verifier si le titre existe deja
    req = db_search(
        """SELECT * FROM tpCollections WHERE titre='%s'""" % (titre))

    for r in req:
        return "Le titre attribué existe déjà. Merci de changer le nom de la collection.", 401

    # Requete pour inserer les donnees
    req = "INSERT INTO tpCollections (titre) VALUES ('%s')" % (titre)

    # Inserer en bdd
    db_add(req)

    # Renvoie resultat
    return "La collection a bien été crée", 201


@app.route("/creer-profil-connu", methods=["POST"])
def profil():

    # Recuperer les donnees
    alias = escape(request.form["alias"])
    prenom = escape(request.form["prenom"])
    nom = escape(request.form["nom"])
    age = escape(request.form["age"])
    sexe = escape(request.form["sexe"])
    education = escape(request.form["education"])
    sociale = escape(request.form["sociale"])
    commentaire = escape(request.form["commentaire"])
    typeP = escape(request.form["typeP"])

    # Requete de donnees
    req = """INSERT INTO tpProfils (type, alias, prenom, nom, age, sexe, education, sociale, commentaire)
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (typeP, alias, prenom, nom, age, sexe, education, sociale, commentaire)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return alias


@app.route("/ready-to-post", methods=["POST"])
def readyToPost():
    alias = escape(request.form["alias"])
    return "Vous avez envoyé : " + alias, 201


@app.route("/modifier-profil", methods=["POST"])
def modifierProfil():

    # Recuperer les donnees
    alias = escape(request.form["alias"])
    prenom = escape(request.form["prenom"])
    nom = escape(request.form["nom"])
    age = escape(request.form["age"])
    sexe = escape(request.form["sexe"])
    education = escape(request.form["education"])
    sociale = escape(request.form["sociale"])
    commentaire = escape(request.form["commentaire"])
    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    UPDATE tpProfils
    SET alias='%s', prenom='%s', nom='%s', age='%s', sexe='%s', education='%s', sociale='%s', commentaire='%s'
    WHERE id=%s""" % (alias, prenom, nom, age, sexe, education, sociale, commentaire, idElement)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return alias


@app.route("/modifier-collection", methods=["POST"])
def modifierCollectionO():

    # Recuperer les donnees
    commentaire = escape(request.form["commentaire"])
    titre = escape(request.form["titre"])
    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    UPDATE tpCollections
    SET commentaire='%s', titre='%s'
    WHERE id=%s""" % (commentaire, titre, idElement)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return "ok"


@app.route("/modifier-dossier", methods=["POST"])
def modifierDossier():

    # Recuperer les donnees
    commentaire = escape(request.form["commentaire"])
    titre = escape(request.form["titre"])
    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    UPDATE tpDossiers
    SET commentaire='%s', titre='%s'
    WHERE id=%s""" % (commentaire, titre, idElement)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return "ok"


@app.route("/modifier-collection", methods=["POST"])
def modifierCollection():

    # Recuperer les donnees
    commentaire = escape(request.form["commentaire"])
    titre = escape(request.form["titre"])
    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    UPDATE tpCollections
    SET commentaire='%s', titre='%s'
    WHERE id=%s""" % (commentaire, titre, idElement)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return "ok"


@app.route("/modifier-texte", methods=["POST"])
def modifierTexte():

    # Recuperer les donnees
    alias = escape(request.form["alias"])
    paternite = escape(request.form["paternite"])
    specification = escape(request.form["specification"])
    typeEcriture = escape(request.form["typeEcriture"])
    segmentation = escape(request.form["segmentation"])
    registre = escape(request.form["registre"])
    commentaire = escape(request.form["commentaire"])
    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    UPDATE tpTexte
    SET titre='%s', paternite='%s', specification='%s', typeEcriture='%s', segmentation='%s', registre='%s', commentaire='%s'
    WHERE id=%s""" % (alias, paternite, specification, typeEcriture, segmentation, registre, commentaire, idElement)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return alias


@app.route("/textesbyprofil", methods=["POST"])
def textesbyprofil():

    # Recuperer les donnees
    idProfil = escape(request.form["id"])

    # Requete de donnees
    req = "SELECT * FROM tpAssociationProfilTextes WHERE id_profil = %s" % (
        idProfil)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage infos
    statsTexte = ""
    for r in data:
        req = "SELECT * FROM tpTexte WHERE id = %s" % (r[1])
        dataTexte = db_search(req)
        for t in dataTexte:
            statsTexte += """
              <tr>
                <th scope="row">%s</th>
                <td>---</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
                <td>%s</td>
              </tr>
            """ % (t[2], t[4], t[6], t[7], t[8])

    # Faire un retour de resultat
    return statsTexte, 201


@app.route("/assoc", methods=["POST"])
def assoc():

    # Recuperer les donnees
    idElement = escape(request.form["id"])
    typeElement = escape(request.form["type"])
    getElement = escape(request.form["get"])

    # Requete de donnees
    req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s' AND champs2 = '%s'" % (
        idElement, typeElement, getElement)
    #req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s' AND champs2 = '%s'" % (idElement, typeElement, getElement)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage infos
    statsTexte = "["
    idEl = 1
    for r in data:
        if r[1] == "Texte" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "%s",
                    "alias": "%s",
                    "nom": "%s",
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[9], t[1], t[2] + " " + nom, r[0])
                idEl += 1
        if r[1] == "Collection" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "Profil %s",
                    "alias": "%s",
                    "nom": "%s",
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[9], t[1], t[2] + " " + nom, r[0])
                idEl += 1
        if r[1] == "Collection" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "Texte",
                    "titre": "%s",
                    "version": 1,
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[2], r[0])
                idEl += 1
        if r[1] == "Collection" and r[2] == "Dossier":
            req = "SELECT * FROM tpDossiers WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "Dossier",
                    "titre": "%s",
                    "commentaire": "%s",
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[1], t[2], r[0])
                idEl += 1
        if r[1] == "Dossier" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "Texte",
                    "titre": "%s",
                    "version": 1,
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[2], r[0])
                idEl += 1
        if r[1] == "Dossier" and r[2] == "Collection":
            req = "SELECT * FROM tpCollections WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "cle_id": %s,
                    "type": "Collection",
                    "titre": "%s",
                    "commentaire": "%s",
                    "delete": %s
                }
                """ % (str(idEl), r[4], t[1], t[2], r[0])
                idEl += 1
        if r[1] == "Dossier" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                if idEl is not 1:
                    statsTexte += ","
                statsTexte += """
                {
                    "id": %s,
                    "type": "Profil %s",
                    "cle_id": %s,
                    "alias": "%s",
                    "nom": "%s",
                    "delete": %s
                }
                """ % (str(idEl), t[9], r[4], t[1], t[2] + " " + nom, r[0])
                idEl += 1
    statsTexte += "]"
    #result = json.loads(statsTexte)

    # Faire un retour de resultat
    return jsonify(statsTexte), 201


@app.route("/resultassocoiation", methods=["POST"])
def resultassocoiation():

    # Recuperer les donnees
    idElement = escape(request.form["id"])
    typeElement = escape(request.form["type"])
    getElement = escape(request.form["get"])

    # Requete de donnees
    req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s' AND champs2 = '%s'" % (
        idElement, typeElement, getElement)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage infos
    statsTexte = ""
    for r in data:
        if r[1] == "Collection" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsTexte += """
                <tr>
                    <th scope="row">Profil %s</th>
                    <td>%s</td>
                    <td>%s</td>
                    <td><button class="delete-associationc" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (t[9], t[1], t[2] + " " + nom, r[0])
        if r[1] == "Dossier" and r[2] == "Profil":
            req = "SELECT * FROM tpProfils WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsTexte += """
                <tr>
                    <th scope="row">Profil %s</th>
                    <td>%s</td>
                    <td>%s</td>
                    <td><button class="delete-association" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (t[9], t[1], t[2] + " " + nom, r[0])
        if r[1] == "Collection" and r[2] == "Dossier":
            req = "SELECT * FROM tpDossiers WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[1])
                statsTexte += """
                <tr>
                    <th scope="row">%s</th>
                    <td>-</td>
                    <td>-</td>
                    <td><button class="delete-associationc" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (nom, r[0])
        if r[1] == "Dossier" and r[2] == "Collection":
            req = "SELECT * FROM tpCollections WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[1])
                statsTexte += """
                <tr>
                    <th scope="row">%s</th>
                    <td>-</td>
                    <td>-</td>
                    <td><button class="delete-association" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (nom, r[0])
        if r[1] == "Collection" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsTexte += """
                <tr>
                    <th scope="row">%s</th>
                    <td>1</td>
                    <td><button class="delete-associationc" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (t[2], r[0])
        if r[1] == "Dossier" and r[2] == "Texte":
            req = "SELECT * FROM tpTexte WHERE id = %s" % (r[4])
            dataTexte = db_search(req)
            for t in dataTexte:
                nom = str(t[3])
                statsTexte += """
                <tr>
                    <th scope="row">%s</th>
                    <td>1</td>
                    <td><button class="delete-association" id="del-element-%s">Supprimer</button></td>
                </tr>
                """ % (t[2], r[0])

    # Faire un retour de resultat
    return statsTexte, 201


@app.route("/importer-texte-bdd", methods=["POST"])
def texte():

    # Recuperer les donnees
    fichier = escape(request.form["fichier"])
    titre = escape(request.form.get("titre", False))
    paternite = escape(request.form.get("paternite", False))
    typeDocument1 = escape(request.form.get("typeDocument1", False))
    typeDocument2 = escape(request.form.get("typeDocument2"))
    typeDocument3 = escape(request.form.get("typeDocument3", False))
    specification = escape(request.form.get("specification", False))
    typeEcriture = escape(request.form.get("typeEcriture", False))
    segmentation = escape(request.form.get("segmentation", False))
    langue = escape(request.form.get("langue", False))
    registre = escape(request.form.get("registre", False))
    commentaire = escape(request.form.get("commentaire", False))

    # Requete de donnees
    req = """INSERT INTO tpTexte (fichier, titre, paternite, typeDocument1, typeDocument2, typeDocument3, specification, typeEcriture, segmentation, langue, registre, commentaire)
    VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (fichier, titre, paternite, typeDocument1, typeDocument2, typeDocument3, specification, typeEcriture, segmentation, langue, registre, commentaire)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return titre, 201


@app.route("/associer-profil-texte", methods=["POST"])
def associerProfilTexte():

    # Recuperer les donnees
    id_texte = escape(request.form["id_texte"])
    id_profil = escape(request.form["id_profil"])

    # Requete de donnees
    req = """INSERT INTO tpAssociationProfilTextes (id_texte, id_profil)
    VALUES ('%s', '%s')""" % (id_texte, id_profil)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return "Done", 201


@app.route("/associer-generalement", methods=["POST"])
def associerGeneralement():

    # Recuperer les donnees
    champs1 = escape(request.form["champs1"])
    champs2 = escape(request.form["champs2"])
    idchamps1 = escape(request.form["idchamps1"])
    idchamps2 = escape(request.form["idchamps2"])

    # Verifier si le titre existe deja
    req = db_search("""SELECT * FROM tpAssociationGenerale WHERE champs1='%s' AND champs2='%s' AND idchamps1=%s AND idchamps2=%s""" %
                    (champs1, champs2, idchamps1, idchamps2))

    for r in req:
        return "L'assocoiation existe déjà.", 401

    # Requete de donnees
    req = """INSERT INTO tpAssociationGenerale (champs1, champs2, idchamps1, idchamps2)
    VALUES ('%s', '%s', %s, %s)""" % (champs1, champs2, idchamps1, idchamps2)

    # Executer la requete
    db_add(req)

    # Faire un retour de resultat
    return "Done", 201


@app.route("/search", methods=["POST", "GET"])
def search():

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils WHERE alias LIKE '%" + "" + "%'")

    # Faire un retour de resultat
    return json.dumps(req)


@app.route("/supprimer-profil", methods=["POST"])
def supprimerProfil():

    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    DELETE FROM tpProfils
    WHERE id = %d""" % (int(idElement))

    # Executer la requete
    db_add(req)

    return "Element supprimé.", 201


@app.route("/supprimer-association", methods=["POST"])
def supprimerAssociation():

    idElement = escape(request.form["id"])

    # Requete de donnees
    req = "SELECT * FROM tpAssociationGenerale WHERE id = %s" % (idElement)

    # Executer la requete
    data = db_search(req)

    # Lire les infos
    if not data:
        return "", 201

    # Stockage infos
    myId = 0
    for r in data:
        myId = r[3]

    # Requete de donnees
    req = """
    DELETE FROM tpAssociationGenerale
    WHERE id = %d""" % (int(idElement))

    # Executer la requete
    db_add(req)

    return str(myId), 201


@app.route("/supprimer-texte", methods=["POST"])
def supprimerTexte():

    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    DELETE FROM tpTexte
    WHERE id = %d""" % (int(idElement))

    # Executer la requete
    db_add(req)

    return "Element supprimé.", 201


@app.route("/supprimer-dossier", methods=["POST"])
def supprimerDossier():

    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    DELETE FROM tpDossiers
    WHERE id = %d""" % (int(idElement))

    # Executer la requete
    db_add(req)

    return "Element supprimé.", 201


@app.route("/supprimer-collection", methods=["POST"])
def supprimerCollection():

    idElement = escape(request.form["id"])

    # Requete de donnees
    req = """
    DELETE FROM tpCollections
    WHERE id = %d""" % (int(idElement))

    # Executer la requete
    db_add(req)

    return "Element supprimé.", 201


@app.route("/searchbyid", methods=["POST", "GET"])
def searchbyid():

    # Recuperer les donnees
    req = request.form["req"]
    #req = "1"

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils WHERE id = " + req + "")

    # Si vide
    if not req:
        req = db_search("SELECT * FROM tpProfils")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        age = "0"
        if r[4] is not "":
            age = r[4]
        result += '{"type": "Profil", "typeP": "%s", "alias": "%s", "id": %s, "prenom": "%s", "nom": "%s", "age": "%s", "sexe": "%s", "education": "%s", "sociale": "%s", "commentaire": "%s"}' % (
            r[9], r[1], str(r[0]), r[2], r[3], str(age), r[5], r[6], r[7], r[8])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-versions", methods=["POST", "GET"])
def searchversions():

    # Recuperer les donnees
    if request.method == 'POST':
        req = request.form["reqText"]
        req = db_search("SELECT * FROM tpVersions WHERE idText = " + req + "")
    else:
        req = db_search("SELECT * FROM tpVersions")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"id": %s, "pretraitement": "%s", "specification": "%s", "link": "%s"}' % (
            str(r[0]), r[1], r[2], r[4])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-analyses", methods=["POST", "GET"])
def searchanalyses():

    # Recuperer les donnees
    if request.method == 'POST':
        req = request.form["reqText"]
        req = db_search("SELECT * FROM tpAnalyses WHERE idText = " + req + "")
    else:
        req = db_search("SELECT * FROM tpAnalyses")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"id": %s, "analyse": "%s", "specification": "%s", "link": "%s"}' % (
            str(r[0]), r[1], r[2], r[4])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-texte", methods=["POST", "GET"])
def searchtexte():

    # Recuperer les donnees
    req = request.form["req"]
    #req = "1"

    # Recherche en DB
    req = db_search("SELECT * FROM tpTexte WHERE id = " + req + "")

    # Si vide
    if not req:
        req = db_search("SELECT * FROM tpTexte")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Texte", "id": %s, "fichier": "%s", "titre": "%s", "paternite": "%s", "typeDocument1": "%s", "specification": "%s", "typeEcriture": "%s", "segmentation": "%s", "langue": "%s", "registre": "%s", "commentaire": "%s", "typeDocument2": "%s", "typeDocument3": "%s"}' % (
            str(r[0]), r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-dossier", methods=["POST", "GET"])
def searchdossier():

    # Recuperer les donnees
    req = request.form["req"]
    #print("*** The req is :", req)
    #req = "1"

    # Recherche en DB

    # Si vide
    if not req:
        req = db_search("SELECT * FROM tpDossiers")
    else:
        req = db_search("SELECT * FROM tpDossiers WHERE id = " + req + "")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Dossiers", "id": %s, "titre": "%s", "commentaire": "%s"}' % (
            str(r[0]), r[1], r[2])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-collection", methods=["POST", "GET"])
def searchcollection():

    # Recuperer les donnees
    req = request.form["req"]
    #req = "1"

    # Recherche en DB
    req = db_search("SELECT * FROM tpCollections WHERE id = " + req + "")

    # Si vide
    if not req:
        req = db_search("SELECT * FROM tpCollections")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Collections", "id": %s, "titre": "%s", "commentaire": "%s"}' % (
            str(r[0]), r[1], r[2])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/verifier-texte", methods=["POST"])
def verifierTexte():
    if request.method == 'POST':

        # Ajout du fichier
        path = 'static/textes'
        ts = calendar.timegm(time.gmtime())
        f = request.files['importer-texte']
        name = str(ts) + ".txt"
        fa = os.path.join(path, name)
        f.save(fa)

        # Detection du fichier
        content = open(fa, 'rb').read()
        result = chardet.detect(content)
        print(result['encoding'])
        if (result['encoding'] != "utf-8"):
            if (result['encoding'] == "ISO-8859-1"):
                content = content.decode('iso-8859-1').encode('utf8')
                # return "Le fichier doit être en UTF-8", 405
            elif (result['encoding'] == "UTF-8-SIG"):
                return "Fichier conforme", 200
            else:
                # return "Le fichier doit être codé en UTF-8", 405
                return "Fichier conforme", 200
        content = content.decode('utf8')

        # Texte que l'on va ouvrir
        #content = open(fa, "r")
        #texte = content.read().encode('utf8')
        # content.close()

        print(content)
        # texte = content

        # Supprimer le document du dossier static
        os.remove(fa)

        # Verifier que le texte ne contient pas de signes interdits
        # if ">" in texte:
        #     return "Fichier non conforme", 405

        # if "<" in texte:
        #     return "Fichier non conforme", 405

        # Si tout se passe bien
        return "Fichier conforme", 200


@app.route("/champs-personnalises-resultat", methods=["POST"])
def champsPersonnalisesResultat():

    # Recuperer les donnees
    req = request.form["id"]
    #req = "1"

    # Recherche en DB
    req = db_search(
        "SELECT * FROM tpChampsPersonnalisesProfil WHERE idProfil = " + req)

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"id": %s, "nomChamps": "%s", "contenu": "%s", "idProfil": "%s"}' % (
            r[0], r[1], r[2], r[3])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/ajouter-champs-personnalises", methods=["POST"])
def ajouterChampsPersonnalises():

    # Parametres
    id_profil = request.form["id"]
    contenu = request.form["contenu"]

    # Ajouter
    req = """
    INSERT INTO tpChampsPersonnalisesProfil (idProfil, contenu)
    VALUES (%s, '%s')""" % (id_profil, contenu)

    # Enregistrer le type de profil
    db_add(req)

    # Message
    return "Champs personnalisés bien ajouté", 201


@app.route("/supprimer-champs-personnalises", methods=["POST"])
def supprimerChampsPersonnalises():

    # Parametres
    id_profil = request.form["id"]

    # Delete
    req = """
    DELETE FROM tpChampsPersonnalisesProfil
    WHERE idProfil = %s""" % (id_profil)

    # Enregistrer le type de profil
    db_add(req)

    # Message
    return "Champs personnalisés bien supprimés", 201


@app.route("/changer-type-profil", methods=["POST"])
def changerTypeProfil():

    # Parametres
    id_profil = request.form["id"]
    type_profil = request.form["type"]

    # Changement type profil
    if type_profil == "anonyme":
        type_profil = "connu"
    else:
        type_profil = "anonyme"

    # Update
    req = """
    UPDATE tpProfils
    SET type='%s'
    WHERE id=%s""" % (type_profil, id_profil)

    # Enregistrer le type de profil
    db_add(req)

    # Retourner un message
    return "Type de profil modifié avec succès", 201


@app.route("/importer-texte", methods=["POST"])
def importerTexte():
    if request.method == 'POST':

        # Ajout du fichier
        path = 'static/textes'
        ts = calendar.timegm(time.gmtime())
        f = request.files['importer-texte']
        name = str(ts) + ".txt"
        name_return = str(ts)
        fa = os.path.join(path, name)
        f.save(fa)
        content = open(fa, "rb").read()
        result = chardet.detect(content)
        if (result['encoding'] != "utf-8"):
            if (result['encoding'] == "ISO-8859-1"):
                content = content.decode('iso-8859-1').encode('utf8')
                # return "Le fichier doit être en UTF-8", 405
            elif (result['encoding'] == "UTF-8-SIG"):
                print("Alright")
                # return "Fichier conforme", 200
            # else:
            #     return "Le fichier doit être codé en UTF-8", 405
        content = content.decode('utf8')
        fi = open(fa, "w")
        fi.write(content)
        fi.close()

        # Premieres analyses
        analyse_global(fa, "1", "1")

        # Detecter langue
        content = open(fa, "r")
        texte = content.read()
        content.close()
        langue = detect(texte)

        # Affichage langue
        if (langue == 'fr'):
            langue = "Français"
        elif (langue == 'es'):
            langue = "Espagnol"
        elif (langue == 'en'):
            langue = "Anglais"
        else:
            langue = "Non spécifiée"

        # Return
        return jsonify(
            langue=langue,
            name=name_return
        )
        # return name_return, 201

    # return "Problem"


@app.route("/test", methods=["POST", "GET"])
def test():

    # Recuperer les donnees
    if request.method == 'POST':
        form = request.form["req"]
    else:
        form = ""

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils WHERE alias LIKE '%" + form +
                    "%' OR nom LIKE '%" + form + "%' OR prenom LIKE '%" + form + "%'")
    req2 = db_search("SELECT * FROM tpTexte WHERE titre LIKE '%" + form + "%'")
    req3 = db_search(
        "SELECT * FROM tpDossiers WHERE titre LIKE '%" + form + "%'")
    req4 = db_search(
        "SELECT * FROM tpCollections WHERE titre LIKE '%" + form + "%'")

    # Boucle
    result = '['
    i = 0
    for r in req2:
        if i > 0:
            result += ","
        result += '{"type": "Texte", "id": %s, "fichier": "%s", "titre": "%s", "paternite": "%s", "typeDocument1": "%s", "specification": "%s", "typeEcriture": "%s", "segmentation": "%s", "langue": "%s", "registre": "%s", "commentaire": "%s", "typeDocument2": "%s", "typeDocument3": "%s"}' % (
            escape(str(r[0])), escape(r[1]), escape(r[2]), escape(r[3]), escape(r[4]), escape(r[5]), escape(r[6]), escape(r[7]), escape(r[8]), escape(r[9]), escape(r[10]), escape(r[11]), escape(r[12]))
        i += 1
    for r in req3:
        if i > 0:
            result += ","
        result += '{"type": "Dossiers", "id": %s, "titre": "%s"}' % (
            escape(str(r[0])), escape(r[1]))
        i += 1
    for r in req4:
        if i > 0:
            result += ","
        result += '{"type": "Collections", "id": %s, "titre": "%s"}' % (
            escape(str(r[0])), escape(r[1]))
        i += 1
    for r in req:
        if i > 0:
            result += ","
        age = "0"
        if r[4] is not "":
            age = r[4]
        result += '{"type": "Profil", "typeP": "%s", "alias": "%s", "id": %s, "prenom": "%s", "nom": "%s", "age": "%s", "sexe": "%s", "education": "%s", "sociale": "%s", "commentaire": "%s"}' % (
            escape(r[9]), escape(r[1]), escape(str(r[0])), escape(r[2]), escape(r[3]), escape(str(age)), escape(r[5]), escape(r[6]), escape(r[7]), escape(r[8]))
        i += 1
    result += "]"

    # Resultat
    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/search-profil", methods=["POST", "GET"])
def searchmyprofil():

    # Recuperer les donnees
    req = request.form["req"]
    #req = "1"

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils WHERE id = " + req + "")

    # Si vide
    if not req:
        req = db_search("SELECT * FROM tpProfils")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        age = "0"
        if r[4] is not "":
            age = r[4]
        result += '{"type": "Profil", "typeP": "%s", "alias": "%s", "id": %s, "prenom": "%s", "nom": "%s", "age": "%s", "sexe": "%s", "education": "%s", "sociale": "%s", "commentaire": "%s"}' % (
            r[9], r[1], str(r[0]), r[2], r[3], str(age), r[5], r[6], r[7], r[8])
        i += 1
    result += "]"

    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/searchprofil", methods=["POST", "GET"])
def searchprofil():

    # Recuperer les donnees
    if request.method == 'POST':
        form = request.form["req"]
    else:
        form = ""

    # Recherche en DB
    req = db_search("SELECT * FROM tpProfils WHERE alias LIKE '%" + form +
                    "%' OR nom LIKE '%" + form + "%' OR prenom LIKE '%" + form + "%'")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        age = "0"
        if r[4] is not "":
            age = r[4]
        result += '{"type": "Profil", "typeP": "%s", "alias": "%s", "id": %s, "prenom": "%s", "nom": "%s", "age": "%s", "sexe": "%s", "education": "%s", "sociale": "%s", "commentaire": "%s"}' % (
            r[9], r[1], str(r[0]), r[2], r[3], str(age), r[5], r[6], r[7], r[8])
        i += 1
    result += "]"

    # Resultat
    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/searchtextes", methods=["POST", "GET"])
def searchetextes():

    # Recuperer les donnees
    if request.method == 'POST':
        form = request.form["req"]
    else:
        form = ""

    # Recherche en DB
    req = db_search("SELECT * FROM tpTexte WHERE titre LIKE '%" + form + "%'")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Texte", "id": %s, "fichier": "%s", "titre": "%s", "paternite": "%s", "typeDocument1": "%s", "specification": "%s", "typeEcriture": "%s", "segmentation": "%s", "langue": "%s", "registre": "%s", "commentaire": "%s", "typeDocument2": "%s", "typeDocument3": "%s"}' % (
            str(r[0]), r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
        i += 1
    result += "]"

    # Resultat
    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/searchcollections", methods=["POST", "GET"])
def searchcollections():

    # Recuperer les donnees
    if request.method == 'POST':
        form = request.form["req"]
    else:
        form = ""

    # Recherche en DB
    req = db_search(
        "SELECT * FROM tpCollections WHERE titre LIKE '%" + form + "%'")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Collections", "id": %s, "titre": "%s", "commentaire": "%s"}' % (
            str(r[0]), r[1], r[2])
        i += 1
    result += "]"

    # Resultat
    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)


@app.route("/searchthedossiers", methods=["POST", "GET"])
def searchthedossiers():

    # Recuperer les donnees
    if request.method == 'POST':
        form = request.form["req"]
    else:
        form = ""

    # Recherche en DB
    req = db_search(
        "SELECT * FROM tpDossiers WHERE titre LIKE '%" + form + "%'")

    # Boucle
    result = '['
    i = 0
    for r in req:
        if i > 0:
            result += ","
        result += '{"type": "Dossiers", "id": %s, "titre": "%s", "commentaire": "%s"}' % (
            str(r[0]), r[1], r[2])
        i += 1
    result += "]"

    # Resultat
    result = json.loads(result)

    # Faire un retour de resultat
    return jsonify(result)
