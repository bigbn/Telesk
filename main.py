#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

import gettext
import sys
import os, logging
from PyQt4 import QtCore, QtGui
from debug import debug

VERSION = "0.1.0"
from forms.dialer import Dialer

def main():
    gettext.textdomain('telesk')
    gettext.install('telesk', './locale', unicode=True)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    wnd = Dialer()
    rc = app.exec_()
    sys.exit(rc)


if __name__ == "__main__":
    main()
