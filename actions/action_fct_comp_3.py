import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic


# Classe permettant d'afficher la fonction à compléter 3
class AppFctComp3(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_comp_3.ui", self)
        self.data = data
        self.loadCategoriesInComboBox()


    # Fonction de chargement des categories dans la liste déroulante
    def loadCategoriesInComboBox(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("SELECT DISTINCT categorieEp FROM LesEpreuves")
        except Exception as e:
            self.ui.combobox_fct_comp_3.clear()
        else:
            display.refreshGenericCombo(self.ui.combobox_fct_comp_3, result)

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshResult(self):
        # TODO 1.6 : fonction à modifier pour remplacer la zone de saisie par une liste de valeurs issues de la BD une
        #  fois le fichier ui correspondant mis à jour
        display.refreshLabel(self.ui.label_fct_comp_3, "")
        if not self.ui.combobox_fct_comp_3.currentText().strip():
            self.ui.table_fct_comp_3.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_comp_3, "Veuillez indiquer un nom de catégorie")
        else:
            try:
                cursor = self.data.cursor()
                result = cursor.execute(
                    "SELECT numEp, nomEp, formeEp, nomDi, nbSportifsEp, dateEp FROM LesEpreuves WHERE categorieEp = ?",
                    [self.ui.combobox_fct_comp_3.currentText().strip()])
            except Exception as e:
                self.ui.table_fct_comp_3.setRowCount(0)
                display.refreshLabel(self.ui.label_fct_comp_3, "Impossible d'afficher les résultats : " + repr(e))
            else:
                i = display.refreshGenericData(self.ui.table_fct_comp_3, result)
                if i == 0:
                    display.refreshLabel(self.ui.label_fct_comp_3, "Aucun résultat")
