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
from langdetect import detect
import chardet    
import io

#
# Impression avec template
#
@app.route('/imprimer-dossier/<elementId>')
def imprimerDossier(elementId):

    # Declaration variables
    statsTextes = ""
    statsProfils = ""
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
    req = "SELECT * FROM tpAssociationGenerale WHERE idchamps1 = %s AND champs1 = '%s'" % (elementId, 'Dossier')

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

    return render_template('impression.html', titre=titre, statsTextes=statsTextes, statsProfils=statsProfils)