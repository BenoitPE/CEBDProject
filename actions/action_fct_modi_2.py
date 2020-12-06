
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import uic

# Classe permettant d'afficher la fonction d'interrogation 1
class AppFctModi2(QDialog):

    # Signal émis lorsque'un changement dans la base de données et qu'un commit a eu lieu
    dataChanged = pyqtSignal()

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_modi_2.ui", self)
        self.data = data

        self.ui.cb_modifier_epreuve.currentIndexChanged.connect(self.refreshParticipantListModification)
        self.ui.cb_inserer_epreuve.currentIndexChanged.connect(self.refreshParticipantListInsertion)

        self.refreshEpreuveListInsertion()
        self.refreshEpreuveListModification() 
        self.refreshEpreuveListSuppression()

    #------------ Partie Insertion -----------------

    # Fonction de chargement des categories dans la liste déroulante
    @pyqtSlot()
    def refreshEpreuveListInsertion(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT numEp
                FROM LesEpreuves
                WHERE numEp NOT IN (SELECT numEp
                                    FROM LesResultats)""")
        except Exception as e:
            self.ui.cb_inserer_epreuve.clear()
        else:
            display.refreshGenericCombo(self.ui.cb_inserer_epreuve, result)

    # Fonction de chargement de tous les participants
    def refreshParticipantListInsertion(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT numIn
                FROM LesInscriptions
                WHERE numEp = ?""",
                [self.ui.cb_inserer_epreuve.currentText().strip()])
        except Exception as e:
            self.ui.cb_inserer_or.clear()
            self.ui.cb_inserer_argent.clear()
            self.ui.cb_inserer_bronze.clear()
        else:
            self.ui.cb_inserer_or.clear()
            self.ui.cb_inserer_argent.clear()
            self.ui.cb_inserer_bronze.clear()
            for row_num, row_data in enumerate(result, 0):
                self.ui.cb_inserer_or.addItem(str(row_data[0]))
                self.ui.cb_inserer_argent.addItem(str(row_data[0]))
                self.ui.cb_inserer_bronze.addItem(str(row_data[0]))

    def insererResultat(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            medailleOr = self.ui.cb_inserer_or.currentText().strip()
            medailleArgent = self.ui.cb_inserer_argent.currentText().strip()
            medailleBronze = self.ui.cb_inserer_bronze.currentText().strip()

            if ((medailleOr != medailleArgent) and (medailleOr != medailleBronze) and (medailleArgent != medailleBronze)) :
                result = cursor.execute(
                    """INSERT INTO LesResultats (numEp, gold, silver, bronze) VALUES (?, ?, ?, ?)""",
                    [self.ui.cb_inserer_epreuve.currentText(), medailleOr, medailleArgent, medailleBronze])
            else:
                raise Exception("Impossible d'ajouter les résultats : des participants sont identiques")
        except Exception as e:
            self.data.rollback()
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible d'ajouter ce résultat : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_fct_modi_2, "Le résultat a été ajouté")
            self.data.commit()
            self.dataChanged.emit()


    #------------ Partie Modification -----------------

    def refreshEpreuveListModification(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT numEp
                FROM LesResultats""")
        except Exception as e:
            self.ui.cb_modifier_epreuve.clear()
        else:
            display.refreshGenericCombo(self.ui.cb_modifier_epreuve, result)
            self.refreshParticipantListModification()

    def refreshParticipantListModification(self):
        try:
            cursor = self.data.cursor()
            # Requete qui permet d'ajouter l'ensemble des participants d'une epreuve
            result = cursor.execute("""
                SELECT numIn
                FROM LesInscriptions
                WHERE numEp = ?""",
                [self.ui.cb_modifier_epreuve.currentText().strip()])

            # Requete qui permet de selectionner les medaillés actuels
            cursor = self.data.cursor()
            result2 = cursor.execute("""
                SELECT gold, silver, bronze
                FROM LesResultats
                WHERE numEp = ?""",
                [self.ui.cb_modifier_epreuve.currentText().strip()])

        except Exception as e:
            self.ui.cb_modifier_or.clear()
            self.ui.cb_modifier_argent.clear()
            self.ui.cb_modifier_bronze.clear()
        else:
            self.ui.cb_modifier_or.clear()
            self.ui.cb_modifier_argent.clear()
            self.ui.cb_modifier_bronze.clear()
            for row_num, row_data in enumerate(result, 0):
                self.ui.cb_modifier_or.addItem(str(row_data[0]))
                self.ui.cb_modifier_argent.addItem(str(row_data[0]))
                self.ui.cb_modifier_bronze.addItem(str(row_data[0]))
            for row_num, row_data in enumerate(result2, 0):
                self.ui.cb_modifier_or.setCurrentText(str(row_data[0]))
                self.ui.cb_modifier_argent.setCurrentText(str(row_data[1]))
                self.ui.cb_modifier_bronze.setCurrentText(str(row_data[2]))


    def modifierResultat(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            medailleOr = self.ui.cb_modifier_or.currentText().strip()
            medailleArgent = self.ui.cb_modifier_argent.currentText().strip()
            medailleBronze = self.ui.cb_modifier_bronze.currentText().strip()

            if ((medailleOr != medailleArgent) and (medailleOr != medailleBronze) and (medailleArgent != medailleBronze)) :
                result = cursor.execute("""
                UPDATE LesResultats
                SET gold = ?, silver = ?, bronze = ?
                WHERE numEp = ?""",
                [medailleOr, medailleArgent, medailleBronze, self.ui.cb_modifier_epreuve.currentText()])
            else:
                raise Exception("Impossible de modifier les résultats : des participants sont identiques")

        except Exception as e:
            self.data.rollback()
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible de modifier ce résultat : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_fct_modi_2, "Le résultat a été modifié")
            self.data.commit()
            self.dataChanged.emit()


    #------------ Partie Suppression -----------------

    def refreshEpreuveListSuppression(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT numEp
                FROM LesResultats""")
        except Exception as e:
            self.ui.cb_supprimer_epreuve.clear()
        else:
            display.refreshGenericCombo(self.ui.cb_supprimer_epreuve, result)

    def supprimerResultat(self):
        display.refreshLabel(self.ui.label_fct_modi_2, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
            DELETE
            FROM LesResultats
            WHERE numEp = ?""",
            [self.ui.cb_supprimer_epreuve.currentText()])
        except Exception as e:
            self.data.rollback()
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible de supprimer les résultats : " + repr(e))
        else:
            display.refreshLabel(self.ui.label_fct_modi_2, "Les résultats ont été supprimés")
            self.data.commit()
            self.dataChanged.emit()
