
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction d'interrogation 1
class AppFctModi2(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_modi_2.ui", self)
        self.data = data

        # Relatifs a l'insertion
        self.refreshEpreuveListInsertion()
        self.ui.cb_inserer_epreuve.currentIndexChanged.connect(self.refreshParticipantListInsertion)

        # Relatifs a la modification 
        self.refreshEpreuveListModification()
        self.ui.cb_modifier_epreuve.currentIndexChanged.connect(self.refreshParticipantListModification)

        # Relatifs a la suppression 
        self.refreshEpreuveListSuppression()

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
            self.refreshParticipantListInsertion()

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
                self.refreshEpreuveListInsertion()
                self.refreshEpreuveListModification()
                display.refreshLabel(self.ui.label_fct_modi_2, "Le résultat a été ajouté")
            else:
                display.refreshLabel(self.ui.label_fct_modi_2, "Impossible d'ajouter les résultats : des participants sont identiques")

        except Exception as e:
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible d'ajouter ce résultat : " + repr(e))
            self.refreshEpreuveListModification()

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

                display.refreshLabel(self.ui.label_fct_modi_2, "Le résultat a été modifié")
            else:
                display.refreshLabel(self.ui.label_fct_modi_2, "Impossible de modifier les résultats : des participants sont identiques")

        except Exception as e:
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible de modifier ce résultat : " + repr(e))


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

            display.refreshLabel(self.ui.label_fct_modi_2, "Les résultats ont été supprimés")

        except Exception as e:
            display.refreshLabel(self.ui.label_fct_modi_2, "Impossible de supprimer les résultats : " + repr(e))
