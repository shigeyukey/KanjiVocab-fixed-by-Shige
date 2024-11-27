# -*- coding: utf-8 -*-
# Copyright: Ankitects Pty Ltd and contributors
# License: GNU AGPL, version 3 or later; http://www.gnu.org/licenses/agpl.html
# Based off Kieran Clancy's initial implementation.

# This file copied from Anki 2.1.13, minus the hook installation steps.

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


import re

r = r' ?([^ >]+?)\[(.+?)\]'
ruby = r'<ruby><rb>\1</rb><rt>\2</rt></ruby>'

def noSound(repl):
    def func(match):
        if match.group(2).startswith("sound:"):
            # return without modification
            return match.group(0)
        else:
            return re.sub(r, repl, match.group(0))
    return func

def _munge(s):
    return s.replace("&nbsp;", " ")

def kanji(txt, *args):
    return re.sub(r, noSound(r'\1'), _munge(txt))

def kana(txt, *args):
    return re.sub(r, noSound(r'\2'), _munge(txt))

def furigana(txt, *args):
    return re.sub(r, noSound(ruby), _munge(txt))

