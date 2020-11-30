
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction d'interrogation 1
class AppFctInte1(QDialog):

    # Constructeur
    def __init__(self, data:sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_inte_1.ui", self)
        self.data = data
        self.refreshAgeEquipeOrList()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshAgeEquipeOrList(self):
        display.refreshLabel(self.ui.label_fct_inte_1, "")
        try:
            cursor = self.data.cursor()
            result = cursor.execute("""
                SELECT e.numEq, ROUND(AVG(s.ageSp), 2)
                FROM LesEquipiers e
                JOIN LesSportifs s ON e.numSp = s.numSp
                JOIN LesResultats r ON e.numEq = r.gold
                GROUP BY e.numEq""")
        except Exception as e:
            self.ui.table_fct_inte_1.setRowCount(0)
            display.refreshLabel(self.ui.label_fct_inte_1, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_inte_1, result)
            if i == 0:
                display.refreshLabel(self.ui.label_fct_inte_1, "Aucun résultat")
