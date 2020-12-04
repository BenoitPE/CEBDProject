
import sqlite3
from utils import display
from PyQt5.QtWidgets import QDialog, QTableWidgetItem
from PyQt5.QtCore import pyqtSlot, pyqtSignal
from PyQt5 import uic

# Classe permettant d'afficher la fonction d'interrogation 1
class AppFctModi1(QDialog):

	# Signal émis lorsque'un changement dans la base de données et qu'un commit a eu lieu
	dataChanged = pyqtSignal()

	# Constructeur
	def __init__(self, data:sqlite3.Connection):
		super(QDialog, self).__init__()
		self.ui = uic.loadUi("gui/fct_modi_1.ui", self)
		self.data = data

		# Connexion des signaux aux slots
		self.ui.comboBox_fct_modi_1_epreuve_inscription.currentIndexChanged.connect(self.refreshParticipantListInscription)
		self.ui.comboBox_fct_modi_1_epreuve_desinscription.currentIndexChanged.connect(self.refreshParticipantListDesinscription)
		self.ui.pushButton_fct_modi_1_desinscription.clicked.connect(self.desinscrire)
		self.ui.pushButton_fct_modi_1_inscription.clicked.connect(self.inscrire)

		# On rafraichit la liste des epreuves 
		self.refreshEpreuveListInscription()
		self.refreshEpreuveListDesinscription()

	@pyqtSlot()
	def inscrire(self):
		try:
			# On teste si les listes déroulantes ne sont pas vides
			if (self.ui.comboBox_fct_modi_1_epreuve_inscription.count() == 0 or self.ui.comboBox_fct_modi_1_participant_inscription.count() == 0):
				raise Exception("L'épreuve et le numéro de sportif ou d'équipe doivent être renseignées")
			else:
				# On effectue l'insertion d'une inscription dans la base de données
				cursor = self.data.cursor()
				cursor.execute(
					"""
					INSERT INTO LesInscriptions (numIn, numEp)
					VALUES (?,?)
					""",
					[self.ui.comboBox_fct_modi_1_participant_inscription.currentText().strip(),
					self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
				)
		except Exception as e:
			# On met à jour le message d'information concernant l'erreur provoquée et on effectue un rollback
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur lors de l'inscription : " + repr(e))
			self.data.rollback()
		else:
			# On met à jour le message d'information
			if (self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[0] == 'individuelle'):
				display.refreshLabel(self.ui.label_fct_modi_1_information, "Le sportif de numéro " + self.ui.comboBox_fct_modi_1_participant_inscription.currentText().strip() + " est inscrit à l'épreuve de numéro " + self.comboBox_fct_modi_1_epreuve_inscription.currentText().strip())
			else:
				display.refreshLabel(self.ui.label_fct_modi_1_information, "L'équipe de numéro " + self.ui.comboBox_fct_modi_1_participant_inscription.currentText().strip() + " est inscrite à l'épreuve de numéro " + self.comboBox_fct_modi_1_epreuve_inscription.currentText().strip())
			# On commit les modifications dans la base de données
			self.data.commit()
			# On émet le signal qu'un changement a eu lieu dans la base de données
			self.dataChanged.emit()


	@pyqtSlot()
	def desinscrire(self):
		try:
			if (self.ui.comboBox_fct_modi_1_epreuve_desinscription.count() == 0 or self.ui.comboBox_fct_modi_1_participant_desinscription.count() == 0):
				raise Exception("L'épreuve et le numéro de sportif ou d'équipe doivent être renseignées")
			# On effectue la suppression d'une inscription dans la base de données
			cursor = self.data.cursor()
			cursor.execute(
				"""
				DELETE FROM LesInscriptions
				WHERE numEp = ? AND numIn = ?
				""",
				[self.ui.comboBox_fct_modi_1_epreuve_desinscription.currentText().strip(),
				self.ui.comboBox_fct_modi_1_participant_desinscription.currentText().strip()]
			)
		except Exception as e:
			# On met à jour le message d'information concernant l'erreur provoquée et on effectue un rollback
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur lors de la désinscription : " + repr(e))
			self.data.rollback()
		else:
			# On met à jour le message d'information
			if (self.ui.comboBox_fct_modi_1_epreuve_desinscription.currentData()[0] == 'individuelle'):
				display.refreshLabel(self.ui.label_fct_modi_1_information, "Le sportif de numéro " + self.ui.comboBox_fct_modi_1_participant_desinscription.currentText().strip() + " est désinscrit de l'épreuve de numéro " + self.comboBox_fct_modi_1_epreuve_desinscription.currentText().strip())
			else:
				display.refreshLabel(self.ui.label_fct_modi_1_information, "L'équipe de numéro " + self.ui.comboBox_fct_modi_1_participant_desinscription.currentText().strip() + " est désinscrite de l'épreuve de numéro " + self.comboBox_fct_modi_1_epreuve_desinscription.currentText().strip())
			# On commit les modifications dans la base de données
			self.data.commit()
			# On émet le signal qu'un changement a eu lieu dans la base de données
			self.dataChanged.emit()


	@pyqtSlot()
	def refreshParticipantListInscription(self):
		try:
			# On sélectionne les candidats éligibles à l'inscription d'une épreuve en fonction des paramètres suivants :
			# - Categorie
			# - Forme
			# - Nombre d'équipiers
			# On enlève les inscrits à l'épreuve
			cursor = self.data.cursor()
			if self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[0] == 'individuelle':
				if self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1] == 'mixte':
					result = cursor.execute(
						"""
						SELECT numSp
						FROM LesSportifs
						EXCEPT
						SELECT numIn
						FROM LesInscriptions
						WHERE numEp = ?
						ORDER BY numSp
						""",
						[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
					)
				else:
					result = cursor.execute(
						"""
						SELECT numSp
						FROM LesSportifs
						WHERE categorieSp = ?
						EXCEPT
						SELECT numIn
						FROM LesInscriptions
						WHERE numEp = ?
						ORDER BY numSp
						""",
						[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1],
						self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
					)
			else:
				if self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[2] is not None:
					if self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1] == 'mixte':
						result = cursor.execute(
							"""
							SELECT numEq
							FROM LesEquipiers
							GROUP BY numEq
							HAVING COUNT(numEq) = ?
							EXCEPT
							SELECT numIn
							FROM LesInscriptions
							WHERE numEp = ?
							ORDER BY numEq
							""",
							[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[2],
							self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
						)

					else:
						result = cursor.execute(
							"""
							SELECT e.numEq
							FROM LesEquipiers e
							JOIN LesSportifs s ON e.numSp = s.numSp
							WHERE s.categorieSp = ?
							GROUP BY e.numEq
							HAVING COUNT(e.numSp) = ?
							EXCEPT
							SELECT numIn
							FROM LesInscriptions
							WHERE numEp = ?
							ORDER BY e.numEq
							""",
							[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1],
							self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[2],
							self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
						)
				else:
					if self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1] == 'mixte':
						result = cursor.execute(
							"""
							SELECT numEq
							FROM LesEquipiers
							GROUP BY numEq
							EXCEPT
							SELECT numIn
							FROM LesInscriptions
							WHERE numEp = ?
							ORDER BY numEq
							""",
							[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
						)
					else:
						result = cursor.execute(
							"""
							SELECT e.numEq
							FROM LesEquipiers e
							JOIN LesSportifs s ON e.numSp = s.numSp
							WHERE s.categorieSp = ?
							GROUP BY e.numEq
							EXCEPT
							SELECT numIn
							FROM LesInscriptions
							WHERE numEp = ?
							ORDER BY e.numEq
							""",
							[self.ui.comboBox_fct_modi_1_epreuve_inscription.currentData()[1],
							self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip()]
						)
		except Exception as e:
			# On met à jour le message d'information d'erreur et on vide la liste des candidats
			self.ui.comboBox_fct_modi_1_participant_inscription.clear()
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur à la récupération des potentiels participants : " + repr(e))
		else:
			# On met à jour l'affichage
			display.refreshGenericCombo(self.ui.comboBox_fct_modi_1_participant_inscription, result)
			if (self.ui.comboBox_fct_modi_1_participant_inscription.count() == 0):
				display.refreshLabel(self.ui.label_fct_modi_1_information, "Tous les candidats éligibles à l'inscription à l'épreuve " + self.ui.comboBox_fct_modi_1_epreuve_inscription.currentText().strip() + " sont déjà inscrits")
			else:
				display.refreshLabel(self.ui.label_fct_modi_1_information, "")


	@pyqtSlot()
	def refreshParticipantListDesinscription(self):
		try:
			# On sélectionne les inscrits à l'épreuve
			cursor = self.data.cursor()
			result = cursor.execute(
				"""
				SELECT numIn
				FROM LesInscriptions
				WHERE numEp = ?
				ORDER BY numIn
				""",
				[self.ui.comboBox_fct_modi_1_epreuve_desinscription.currentText().strip()]
			)
		except Exception as e:
			# On met à jour le message d'erreur et on vide la liste des inscrits
			self.ui.comboBox_fct_modi_1_participant_desinscription.clear()
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur à la récupération des inscrits : " + repr(e))
		else:
			# On met à jour l'affichage
			display.refreshGenericCombo(self.ui.comboBox_fct_modi_1_participant_desinscription, result)


	def refreshEpreuveListInscription(self):
		try:
			# On sélectionne les épreuves plus la forme, la categorie et le nombre d'équipiers nécessaires
			cursor = self.data.cursor()
			result = cursor.execute(
				"""
				SELECT numEp, formeEp, categorieEp, nbSportifsEp
				FROM LesEpreuves
				ORDER BY numEp
				"""
			)
		except:
			# On met à jour le message d'erreur et on vide la liste des épreuves
			self.ui.comboBox_fct_modi_1_epreuve_inscription.clear()
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur à la récupération des épreuves pour l'inscription : " + repr(e))
		else:
			# On met à jour l'affichage
			self.ui.comboBox_fct_modi_1_epreuve_inscription.clear()
			for row_num, row_data in enumerate(result, 0):
				self.ui.comboBox_fct_modi_1_epreuve_inscription.addItem(str(row_data[0]), (str(row_data[1]), str(row_data[2]), row_data[3]))


	def refreshEpreuveListDesinscription(self):
		try:
			# On sélectionne les épreuves et leur forme
			cursor = self.data.cursor()
			result = cursor.execute(
				"""
				SELECT numEp, formeEp
				FROM LesEpreuves
				ORDER BY numEp
				"""
			)
		except Exception as e:
			# On met à jour l'erreur
			self.ui.comboBox_fct_modi_1_epreuve_desinscription.clear()
			display.refreshLabel(self.ui.label_fct_modi_1_information, "Erreur à la récupération des épreuves pour la désinscription : " + repr(e))
		else:
			# On met à jour l'affichage
			self.ui.comboBox_fct_modi_1_epreuve_desinscription.clear()
			for row_num, row_data in enumerate(result, 0):
				self.ui.comboBox_fct_modi_1_epreuve_desinscription.addItem(str(row_data[0]), (str(row_data[1])))