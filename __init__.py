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


from aqt import mw
from aqt.qt import QAction

try:
    from importlib import reload
except:
    pass #Python 2 has reload built-in

def updateKanjiVocab():
    from . import run
    reload(run)
    run.updateKanjiVocab()

action = QAction("KanjiVocab...", mw)
action.triggered.connect(updateKanjiVocab)
mw.form.menuTools.addAction(action)
