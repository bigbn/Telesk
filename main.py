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
# Foundation, Inc., 59 Temple Place, Suiогоte 330, Boston, MA  02111-1307  USA

import gettext
import gettext_windows
import sys
import os
from PyQt4 import QtGui
from debug import debug
#from forms.login import LoginForm

VERSION = "0.1.0"

from forms.dialer import Dialer
def main():
    if sys.platform.startswith("win"):
        gettext_windows.setup_env()

    lang_path = os.path.dirname(os.path.abspath(sys.argv[0])) + '/locale'
    debug("Lang path: %s" % lang_path)
    gettext.install('telesk', lang_path, unicode=True)
    app = QtGui.QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    d = Dialer()
    d.show()
    #w = LoginForm()
    #w.show()
    rc = app.exec_()
    sys.exit(rc)

if __name__ == "__main__":
    main()
