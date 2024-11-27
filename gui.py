# -*- coding: utf-8 -*-
# Copyright (C) 2015,2017,2019  Helen Foster
# Copyright (C) 2024 Shigeyuki  <http://patreon.com/Shigeyuki>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html

# KanjiVocab is an Anki addon which adds known vocab to a kanji deck.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from aqt.qt import *
from aqt.utils import openLink
from aqt.main import AnkiQt

from copy import deepcopy
from .button_manager import mini_button


class ComboBoxKV(QComboBox):

    def setup(self, dic, key, callback):
        self.setCurrentByText(dic.get(key, ""))
        callback(self.currentText())
        # https://github.com/HelenFoster/KanjiVocab/issues/17
        # self.currentIndexChanged[str].connect(callback)
        self.currentTextChanged.connect(callback)

    def setCurrentByText(self, text, defaultIndex=0):
        index = self.findText(text)
        if index == -1:
            index = defaultIndex
        self.setCurrentIndex(index)


class Count:
    
    def __init__(self, start=0, step=1):
        self.x = start
        self.step = step
    
    def next(self):
        x = self.x
        self.x = x + self.step
        return x


class Settings(QDialog):

    def __init__(self, mw:"AnkiQt", conf, checkConfig):

        QDialog.__init__(self, mw, Qt.WindowType.Window)
        self.mw = mw
        self.conf = deepcopy(conf)
        self.checkConfig = checkConfig

        self.resize(780, 400)
        self.setWindowTitle("KanjiVocab settings fixed by Shige")
        
        self.layoutOuter = QVBoxLayout(self)
        self.tabs = QTabWidget(self)
        self.layoutOuter.addWidget(self.tabs)
        self.tabUpdate = QWidget()
        self.tabScan = QWidget()
        self.tabs.addTab(self.tabUpdate, "Cards to update")
        self.tabs.addTab(self.tabScan, "Cards to scan")
        
        
        self.layoutUpdate = QGridLayout(self.tabUpdate)
        
        r = Count()
        self.layoutUpdate.addWidget(
            QLabel(text="Note type"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="Kanji field (the kanji character by itself)"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="Dictionary words (not scanned)"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="Questions"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="Extra answers"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="Allow ambiguous questions"), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text="<b>Fields to update (the existing contents will be lost!)</b>"), 
            r.next(), 0, 1, 2)
        self.layoutUpdate.addWidget(
            QLabel(text=conf["fieldVocabQuestion"]), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text=conf["fieldVocabResponse"]), r.next(), 0)
        self.layoutUpdate.addWidget(
            QLabel(text=conf["fieldVocabExtra"]), r.next(), 0)
        
        self.pickNoteType = ComboBoxKV()
        self.pickFieldKanji = ComboBoxKV()
        self.pickFreqFilter = ComboBoxKV()
        self.pickNumQuestions = QSpinBox()
        self.pickNumExtra = QSpinBox()
        self.pickAllowAmbig = QCheckBox()
        self.foundFieldQuestion = QLabel()
        self.foundFieldAnswer = QLabel()
        self.foundFieldExtra = QLabel()
        
        r = Count()
        self.layoutUpdate.addWidget(self.pickNoteType, r.next(), 1)
        self.layoutUpdate.addWidget(self.pickFieldKanji, r.next(), 1)
        self.layoutUpdate.addWidget(self.pickFreqFilter, r.next(), 1)
        self.layoutUpdate.addWidget(self.pickNumQuestions, r.next(), 1)
        self.layoutUpdate.addWidget(self.pickNumExtra, r.next(), 1)
        self.layoutUpdate.addWidget(self.pickAllowAmbig, r.next(), 1)
        r.next()
        self.layoutUpdate.addWidget(self.foundFieldQuestion, r.next(), 1)
        self.layoutUpdate.addWidget(self.foundFieldAnswer, r.next(), 1)
        self.layoutUpdate.addWidget(self.foundFieldExtra, r.next(), 1)
        
        
        self.layoutScan = QGridLayout(self.tabScan)
        
        self.layoutScan.addWidget(QLabel(text="Note type"), 0, 0)
        self.layoutScan.addWidget(QLabel(text="Scan type"), 0, 1)
        self.layoutScan.addWidget(QLabel(text="Expression field"), 0, 2)
        self.layoutScan.addWidget(QLabel(text="Reading field"), 0, 3)
        self.layoutScan.addWidget(QLabel(text="Include<br>inactive"), 0, 4)
        
        numScans = self.conf["numScans"]
        self.pickScanNoteTypes = [ComboBoxKV() for i in range(numScans)]
        self.pickScanTypes = [ComboBoxKV() for i in range(numScans)]
        self.pickScanExpressions = [ComboBoxKV() for i in range(numScans)]
        self.pickScanReadings = [ComboBoxKV() for i in range(numScans)]
        self.pickScanInactives = [QCheckBox() for i in range(numScans)]
        self.pickScanColumns = [
            self.pickScanNoteTypes,
            self.pickScanTypes,
            self.pickScanExpressions,
            self.pickScanReadings,
            self.pickScanInactives]
        for row in range(numScans):
            for col in range(5):
                self.layoutScan.addWidget(self.pickScanColumns[col][row], row + 1, col)
        
        
        buttons = QDialogButtonBox()
        buttons.addButton(QDialogButtonBox.StandardButton.Cancel)
        buttons.addButton(QDialogButtonBox.StandardButton.Save)
        buttons.addButton("Run", QDialogButtonBox.ButtonRole.YesRole)
        


        
        self.conf["run"] = False
        def buttonClicked(button):
            role = buttons.buttonRole(button)
            if role == QDialogButtonBox.ButtonRole.YesRole:
                self.checkAndRun()
            elif role == QDialogButtonBox.ButtonRole.AcceptRole:
                self.accept()
            else:
                self.reject()
        buttons.clicked.connect(buttonClicked)
        # self.layoutOuter.addWidget(buttons)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch()
        buttons_layout.addWidget(buttons)
        self.layoutOuter.addLayout(buttons_layout)

        wiki_button = QPushButton("📖Wiki")
        mini_button(wiki_button)
        wiki_button.clicked.connect(lambda: openLink("https://shigeyukey.github.io/shige-addons-wiki/KanjiVocab.html"))

        report_button = QPushButton("🚨Report")
        mini_button(report_button)
        report_button.clicked.connect(lambda: openLink("https://shigeyukey.github.io/shige-addons-wiki/KanjiVocab.html#report"))

        buttons_layout.addWidget(wiki_button)
        buttons_layout.addWidget(report_button)




        if hasattr(self.mw.col.models, "all_names"):
            noteTypeNames = self.mw.col.models.all_names()
        else:
            noteTypeNames = self.mw.col.models.allNames()

        for box in self.pickScanNoteTypes:
            box.addItem("")
        for box in [self.pickNoteType] + self.pickScanNoteTypes:
            for noteTypeName in noteTypeNames:
                box.addItem(noteTypeName)
        
        for box in self.pickScanTypes:
            box.addItem("vocab")
            box.addItem("text")
        
        def pickNoteTypeChanged(text):
            self.conf["noteType"] = text
            self.refillFieldBox(self.pickFieldKanji, text)
            self.updateFieldsToUpdate(text)
        self.pickNoteType.setup(self.conf, "noteType", pickNoteTypeChanged)
        
        def pickFieldKanjiChanged(text):
            self.conf["fieldKanji"] = text
        self.pickFieldKanji.setup(self.conf, "fieldKanji", pickFieldKanjiChanged)
        
        def pickFreqFilterChanged(text):
            self.conf["freqFilter"] = text
        for item in self.conf["freqFilters"]:
            self.pickFreqFilter.addItem(item)
        self.pickFreqFilter.setup(self.conf, "freqFilter", pickFreqFilterChanged)
        
        def pickNumQuestionsChanged(value):
            self.conf["numQuestions"] = value
        self.pickNumQuestions.setValue(self.conf.get("numQuestions", 4))
        pickNumQuestionsChanged(self.pickNumQuestions.value())
        self.pickNumQuestions.valueChanged.connect(pickNumQuestionsChanged)
        
        def pickNumExtraChanged(value):
            self.conf["numExtra"] = value
        self.pickNumExtra.setValue(self.conf.get("numExtra", 4))
        pickNumExtraChanged(self.pickNumExtra.value())
        self.pickNumExtra.valueChanged.connect(pickNumExtraChanged)
        
        def pickAllowAmbigChanged(state):
            self.conf["allowAmbig"] = self.pickAllowAmbig.isChecked()
        self.pickAllowAmbig.setChecked(self.conf.get("allowAmbig", False))
        pickAllowAmbigChanged(None)
        self.pickAllowAmbig.stateChanged.connect(pickAllowAmbigChanged)
        
        scanConfs = self.conf.get("scan", [])
        scanConfs = scanConfs[:numScans]  #discard any scans we can't see
        self.conf["scan"] = scanConfs
        for row in range(numScans):
            if len(scanConfs) <= row:
                scanConfs.append({})
            
            def pickScanNoteTypeChanged(text, r=row):
                scanConfs[r]["noteType"] = text
                self.recalcScanFields(r)
            self.pickScanNoteTypes[row].setup(scanConfs[row], "noteType", pickScanNoteTypeChanged)
            
            def pickScanTypeChanged(text, r=row):
                scanConfs[r]["scanType"] = text
                self.recalcScanFields(r)
            self.pickScanTypes[row].setup(scanConfs[row], "scanType", pickScanTypeChanged)
            
            def pickScanExpressionChanged(text, r=row):
                scanConfs[r]["expression"] = text
            self.pickScanExpressions[row].setup(scanConfs[row], "expression", pickScanExpressionChanged)
            
            def pickScanReadingChanged(text, r=row):
                scanConfs[r]["reading"] = text
            self.pickScanReadings[row].setup(scanConfs[row], "reading", pickScanReadingChanged)
            
            def pickScanInactiveChanged(state, r=row):
                scanConfs[r]["includeInactive"] = self.pickScanInactives[r].isChecked()
            self.pickScanInactives[row].setChecked(scanConfs[row].get("includeInactive", False))
            pickScanInactiveChanged(None)
            self.pickScanInactives[row].stateChanged.connect(pickScanInactiveChanged)


    def lookupFieldNames(self, noteTypeName):
        if hasattr(self.mw.col.models, "by_name"):
            model = self.mw.col.models.by_name(noteTypeName)
        else:
            model = self.mw.col.models.byName(noteTypeName)

        if model is None:
            fieldNames = []  #happens if no model is selected
        else:
            fieldNames = [fld["name"] for fld in model["flds"]]
        return fieldNames

    def refillFieldBox(self, pickField, noteTypeName, optional=False):
        fieldNames = self.lookupFieldNames(noteTypeName)
        pickField.clear()
        if optional and fieldNames != []:
            pickField.addItem("")
        pickField.addItems(fieldNames)
    
    def recalcScanFields(self, row):
        noteTypeName = self.pickScanNoteTypes[row].currentText()
        self.refillFieldBox(self.pickScanExpressions[row], noteTypeName)
        self.pickScanReadings[row].clear()
        if self.pickScanTypes[row].currentText() == "vocab":
            self.refillFieldBox(self.pickScanReadings[row], noteTypeName, optional=True)

    def updateFieldsToUpdate(self, noteTypeName):
        fieldNames = self.lookupFieldNames(noteTypeName)
        def updateLine(widget, fieldName):
            if fieldName in fieldNames:
                text = "found"
            else:
                text = "not found"
            widget.setText(text)
        updateLine(self.foundFieldQuestion, self.conf["fieldVocabQuestion"])
        updateLine(self.foundFieldAnswer, self.conf["fieldVocabResponse"])
        updateLine(self.foundFieldExtra, self.conf["fieldVocabExtra"])
    
    def checkAndRun(self):
        confError = self.checkConfig(self.mw, self.conf)
        if confError:
            msgbox = QMessageBox(QMessageBox.Icon.Warning, "Error", confError, QMessageBox.StandardButton.Ok)
            if hasattr(msgbox, "exec_"):
                msgbox.exec_()
            else:
                msgbox.exec()
        else:
            self.conf["run"] = True
            self.accept()

