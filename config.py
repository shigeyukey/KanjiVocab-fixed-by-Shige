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


import collections, os
from aqt import mw

config = {}



#THESE SETTINGS ARE CHANGED IN THE GUI.
#(They are stored as JSON in the file indicated by config["pathConfigFile"]).

#Update cards with this note type.
config["noteType"] = "Heisig"

#Field used to select cards to update. Should contain only the kanji character being tested.
config["fieldKanji"] = "Kanji"

#One of the keys of "freqFilters", for choosing unscanned dictionary words.
config["freqFilter"] = "none"

#The maximum number of words with masked kanji on each card.
config["numQuestions"] = 4

#The maximum number of extra words on each card.
config["numExtra"] = 4

#Whether to allow questions with more than one likely answer.
config["allowAmbig"] = False

#Cards to scan for known words.
#A note type can appear more than once, with a different field.
#"scanType" can be "vocab" or "text".
#The "vocab" scan considers the expression and reading as-is.
#  If you don't have a reading field, set "reading" to "" (empty string).
#The "text" scan splits the expression with MeCab.
#  ("reading" should be an empty string)
#"includeInactive" is a boolean, indicating whether to scan new and suspended cards.
config["scan"] = []
#This variable is just an example and doesn't do anything:
configScanExample = [
    {
        "noteType": "vocab",
        "scanType": "vocab",
        "expression": "expression",
        "reading": "kana",
        "includeInactive": False
    },
    {
        "noteType": "Nayrs Japanese Core5000",
        "scanType": "text",
        "expression": "Expression",
        "reading": "",
        "includeInactive": True
    }
]



#ADD THESE FIELDS TO YOUR DECK. THE CONTENTS WILL BE OVERWRITTEN WITH EACH RUN.

#Words with masked kanji on the front of the card. FIELD WILL BE OVERWRITTEN.
config["fieldVocabQuestion"] = u"KanjiVocabQuestion"

#Answers to the above questions on the back of the card. FIELD WILL BE OVERWRITTEN. 
config["fieldVocabResponse"] = u"KanjiVocabAnswer"

#Extra vocab on the back of the card. FIELD WILL BE OVERWRITTEN.
config["fieldVocabExtra"] = u"KanjiVocabExtra"



config["numScans"] = 8
config["questionChar"] = u"〇"
config["freezeAnkiTag"] = "KanjiVocabFreeze"

config["allowOverride"] = ["noteType", "fieldKanji", "freqFilter", "numQuestions", "numExtra", "allowAmbig", "scan"]
config["pathDicFile"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), "jmdict_freqs.txt")
config["pathConfigFile"] = os.path.normpath(os.path.join(mw.col.media.dir(), "../KanjiVocab.json"))

#Using '@' to split results.
config["mecabArgs"] = ['--node-format="%m@%f[6]@"']

def wordIsP1(wq):
    p = wq.pris
    return ("gai1" in p or "ichi1" in p or "news1" in p or "spec1" in p or "spec2" in p)

def wordIsP1orP2(wq):
    return (len(wq.pris) > 0)

def questionKey(q):
    return (q.kanjiKnown, q.kanaKnown, q.nf, not wordIsP1orP2(q))

config["questionMatchLikely"] = wordIsP1
config["questionMatchConfuse"] = wordIsP1orP2
config["learnMatchLikely"] = wordIsP1
config["learnMatchConfuse"] = wordIsP1
config["questionKey"] = questionKey
config["questionKeyExtra"] = questionKey

config["freqFilters"] = collections.OrderedDict()
config["freqFilters"]["none"] = lambda q: False
config["freqFilters"]["nf12 (6k words)"] = lambda q: q.nf <= 12
config["freqFilters"]["news1 (12k words)"] = lambda q: q.nf <= 24
config["freqFilters"]["P (18k words)"] = wordIsP1
config["freqFilters"]["P2 (25k words)"] = wordIsP1orP2
config["freqFilters"]["all"] = lambda q: True
