#
# (DB) Creation et execution de base de donnees
# Module Manager - CHEMI IRITA
#

# Importations
import sys
import sqlite3
import os.path
from os import path

# Fonction pour la mise en DB
def db_create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except:
        print("Erreur creation de table :", sys.exc_info()[0])

def db_init():
    # Verifier si le fichier existe
    if (path.exists("data_module_manager.db")):
        # Charger la DB
        print("Chargement de la base de données.")
        db = sqlite3.connect('data_module_manager.db')
        return db
    else:
        # Créer le fichier de la DB
        print("Création d'un fichier pour la base de données.")
        db = sqlite3.connect('data_module_manager.db')

        # Schema DB
        # Nouveau schema
        table_profils = """CREATE TABLE IF NOT EXISTS tpProfils (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                alias TEXT,
                                prenom TEXT,
                                nom TEXT,
                                age TEXT,
                                sexe TEXT,
                                education TEXT,
                                sociale TEXT,
                                commentaire TEXT
                            );
                        """

        # Ancien schema
        sql_create_reftextes_table = """CREATE TABLE IF NOT EXISTS RefTextes (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        titre_texte TEXT NOT NULL
                                    );
                                """

        sql_create_textes_table = """CREATE TABLE IF NOT EXISTS Textes (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        identifiant_texte TEXT NOT NULL,
                                        texte TEXT NOT NULL,
                                        version INTEGER NOT NULL,
                                        commentaire TEXT
                                    );
                                """

        sql_create_profils_table = """CREATE TABLE IF NOT EXISTS Profils (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        commentaire TEXT,
                                        nom TEXT NOT NULL
                                    );
                                """

        sql_create_collections_table = """CREATE TABLE IF NOT EXISTS Collections (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        commentaire TEXT,
                                        nom TEXT NOT NULL
                                    );
                                """

        sql_create_dossiers_table = """CREATE TABLE IF NOT EXISTS Dossiers (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        commentaire TEXT,
                                        nom TEXT NOT NULL
                                    );
                                """

        sql_create_refprofils_table = """CREATE TABLE IF NOT EXISTS RefProfils (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        idProfil INTEGER NOT NULL,
                                        idTexte INTEGER NOT NULL,
                                        FOREIGN KEY (idProfil) REFERENCES Profils (id),
                                        FOREIGN KEY (idTexte) REFERENCES Textes (id)
                                    );
                                """

        sql_create_refcollections_table = """CREATE TABLE IF NOT EXISTS RefCollections (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        idCollection INTEGER NOT NULL,
                                        idTexte INTEGER NOT NULL,
                                        FOREIGN KEY (idCollection) REFERENCES Collections (id),
                                        FOREIGN KEY (idTexte) REFERENCES Textes (id)
                                    );
                                """

        sql_create_refdossiers_table = """CREATE TABLE IF NOT EXISTS RefDossiers (
                                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                                        idDossiers INTEGER NOT NULL,
                                        idTexte INTEGER NOT NULL,
                                        FOREIGN KEY (idDossiers) REFERENCES Dossiers (id),
                                        FOREIGN KEY (idTexte) REFERENCES Textes (id)
                                    );
                                """
        

        # Mise en DB
        # Nouveau DB
        db_create_table(db, table_profils)

        # Anciens DB
        db_create_table(db, sql_create_reftextes_table)
        db_create_table(db, sql_create_textes_table)
        db_create_table(db, sql_create_profils_table)
        db_create_table(db, sql_create_collections_table)
        db_create_table(db, sql_create_dossiers_table)
        db_create_table(db, sql_create_refprofils_table)
        db_create_table(db, sql_create_refcollections_table)
        db_create_table(db, sql_create_refdossiers_table)

        return db

    
def db_request(req):
    return "ok"

def db_add(req):
    try:
        db = db_init()
        c = db.cursor()
        c.execute(req)
        db.commit()
        db.close()
        return "Données ajoutées avec succès."
    except ValueError:
        print("Erreur produite.")

def db_add_last_id(req):
    try:
        db = db_init()
        c = db.cursor()
        c.execute(req)
        db.commit()
        db.close()
        return c.lastrowid
    except ValueError:
        print("Erreur produite.")

def db_search(req):
    try:
        db = db_init()
        c = db.cursor()
        c.execute(req)
        returnValue = c.fetchall()
        db.commit()
        db.close()
        print(returnValue)
        return returnValue
    except ValueError:
        print("Erreur produite.")