
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
        self.loadCategoriesInComboBox()


    # Fonction de chargement des categories dans la liste déroulante
    @pyqtSlot()
    def loadCategoriesInComboBox(self):
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT nomEp
                FROM LesEpreuves""")
        except Exception as e:
            self.ui.combobox_fct_comp_3.clear()
        else:
            display.refreshGenericCombo(self.ui.combobox_fct_comp_3, result)
