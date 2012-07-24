from PyQt4.QtGui import *
from PyQt4.QtCore import Qt

# Copyright (C) 2010-2012 SKAT Ltd. (http://www.scat.su)

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
 
class ClearLineEdit(QLineEdit):
    def __init__(self,parent=None):
        QLineEdit.__init__(self,parent)
        self.button=QToolButton(self)

        self.button.setCursor(Qt.ArrowCursor)
        self.button.hide()
        self.button.setFocusPolicy(Qt.NoFocus)
        self.button.setIcon(QIcon.fromTheme("edit-clear"))
        self.button.setStyleSheet("border: none;")
        self.textChanged.connect(self.changed)
        self.button.clicked.connect(self.clear)
 
        layout=QVBoxLayout(self)
        layout.addWidget(self.button,0,Qt.AlignRight)
        layout.setSpacing(0)
        layout.setMargin(0)
 
    def changed(self,text):
        if len(text)==0: self.button.hide()
        else: self.button.show()
