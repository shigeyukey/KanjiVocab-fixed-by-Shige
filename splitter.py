# -*- coding: utf-8 -*-
# Copyright (C) 2015,2017,2019  Helen Foster
# Copyright (C) 2024 Shigeyuki  <http://patreon.com/Shigeyuki>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
#
# Based on japanese/reading.py
# Copyright: Ankitects Pty Ltd and contributors
# https://ankiweb.net/shared/info/3918629684
#
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


import os, subprocess
try:
    from anki.utils import is_win
    isWin = is_win
except:
    from anki.utils import isWin




class Splitter:
    def __init__(self, mecabArgs):
        try:
            import japanese # type: ignore
        except:
            try:
                japanese = __import__("3918629684")
            except:
                raise Exception('Failed to import Japanese Support module')
        self.jpr = japanese.reading
        try:
            supportDir = self.jpr.supportDir
        except:
            supportDir = "../../addons/japanese/support/"
        
        mecabCmd = self.jpr.mungeForPlatform(
            [os.path.join(supportDir, "mecab")] + mecabArgs + [
                '-d', supportDir, '-r', os.path.join(supportDir,"mecabrc"),
                '-u', os.path.join(supportDir, "user_dic.dic")])
        os.environ['DYLD_LIBRARY_PATH'] = supportDir
        os.environ['LD_LIBRARY_PATH'] = supportDir
        
        try:
            if not isWin:
                os.chmod(mecabCmd[0], 0o755)
            self.mecab = subprocess.Popen(
                mecabCmd, bufsize=-1, stdin=subprocess.PIPE,
                stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                startupinfo=self.jpr.si)
        except OSError:
            raise Exception("Failed to run MeCab at %s" % mecabCmd[0])

    def analyze(self, expr):
        expr = self.jpr.escapeText(expr)
        self.mecab.stdin.write(expr.encode("utf-8", "ignore") + b'\n')
        self.mecab.stdin.flush()
        expr = self.mecab.stdout.readline().rstrip(b'\r\n').decode("utf-8", "replace")
        return expr.split("@")

