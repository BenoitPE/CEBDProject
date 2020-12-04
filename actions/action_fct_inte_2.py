import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic

# Classe permettant d'afficher la fonction d'interrogation 2


class AppFctInte2(QDialog):

    # Constructeur
    def __init__(self, data: sqlite3.Connection):
        super(QDialog, self).__init__()
        self.ui = uic.loadUi("gui/fct_inte_2.ui", self)
        self.data = data
        self.refreshClassementPaysList()

    # Fonction de mise à jour de l'affichage
    @pyqtSlot()
    def refreshClassementPaysList(self):
        display.refreshLabel(self.ui.label_fct_inte_2, "")
        try:
            cursor = self.data.cursor()

            result = cursor.execute("""
            WITH TousLesPays AS (
                SELECT DISTINCT pays
                FROM LesSportifs
            ), LesEquipesPays AS (
                SELECT e.numEq, pays
                FROM LesEquipiers e
                JOIN LesSportifs s ON e.numSp = s.numSp 
                GROUP BY e.numEq
            ), MedaillesOrSportifParPays AS (
                SELECT s.pays, COUNT(r.gold) AS nbOrSportif
                FROM LesResultats r
                JOIN LesSportifs s ON r.gold = s.numSp
                GROUP BY s.pays
            ), MedaillesArgentSportifParPays AS (
                SELECT s.pays, COUNT(r.silver) AS nbArgentSportif
                FROM LesResultats r
                JOIN LesSportifs s ON r.silver = s.numSp
                GROUP BY s.pays
            ), MedaillesBronzeSportifParPays AS (
                SELECT s.pays, COUNT(r.bronze) AS nbBronzeSportif
                FROM LesResultats r
                JOIN LesSportifs s ON r.bronze = s.numSp
                GROUP BY s.pays
            ), MedaillesOrEquipesParPays AS (
                SELECT e.pays, COUNT(r.gold) AS nbOrEquipe
                FROM LesResultats r
                JOIN LesEquipesPays e ON r.gold = e.numEq
                GROUP BY e.pays
            ), MedaillesArgentEquipesParPays AS (
                SELECT e.pays, COUNT(r.silver) AS nbArgentEquipe
                FROM LesResultats r
                JOIN LesEquipesPays e ON r.silver = e.numEq
                GROUP BY e.pays
            ), MedaillesBronzeEquipesParPays AS (
                SELECT e.pays, COUNT(r.bronze) AS nbBronzeEquipe
                FROM LesResultats r
                JOIN LesEquipesPays e ON r.bronze = e.numEq
                GROUP BY e.pays
            )
            SELECT p.pays, (ifnull(osp.nbOrSportif, 0) + ifnull(oeq.nbOrEquipe, 0)) AS nbOrPays, (ifnull(asp.nbArgentSportif, 0) + ifnull(aeq.nbArgentEquipe, 0)) AS nbArgentPays, (ifnull(bsp.nbBronzeSportif, 0) + ifnull(beq.nbBronzeEquipe, 0)) AS nbBronzePays
            FROM TousLesPays p
            LEFT JOIN MedaillesOrSportifParPays osp ON p.pays = osp.pays
            LEFT JOIN MedaillesArgentSportifParPays asp ON p.pays = asp.pays
            LEFT JOIN MedaillesBronzeSportifParPays bsp ON p.pays = bsp.pays
            LEFT JOIN MedaillesOrEquipesParPays oeq ON p.pays = oeq.pays
            LEFT JOIN MedaillesArgentEquipesParPays aeq ON p.pays = aeq.pays
            LEFT JOIN MedaillesBronzeEquipesParPays beq ON p.pays = beq.pays
            GROUP BY p.pays
            ORDER BY nbOrPays DESC, nbArgentPays DESC, nbBronzePays DESC
            """)

        except Exception as e:
            self.ui.table_fct_inte_2.setRowCount(0)
            display.refreshLabel(
                self.ui.label_fct_inte_2, "Impossible d'afficher les résultats : " + repr(e))
        else:
            i = display.refreshGenericData(self.ui.table_fct_inte_2, result)
            if i == 0:
                display.refreshLabel(
                    self.ui.label_fct_inte_2, "Aucun résultat")
