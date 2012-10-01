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

from StringIO import StringIO
import os, sys
from debug import debug

def profile_path(filename):
    if filename is not None:
        if not sys.platform.startswith("win"):
            path = os.path.expanduser("~") + "/.skat"
            if not os.path.exists(path):
                os.makedirs(path)
            FILE = os.path.join(path, filename)
        else:
            path = os.path.expanduser("~") + "\\skat"
            if not os.path.exists(path):
                os.makedirs(path)    
            FILE = "%s\\%s" % (path,filename)
    return FILE

CKEY = "Jksaa68snHa[pewmxTgsoiq-234sjs;sa032ngldf"
SETTINGS_FILE = profile_path("settings.conf")

def mycrypt(aString, key):
    kIdx = 0
    cryptStr = ""
    for x in range(len(aString)):
        cryptStr = cryptStr + \
                   chr( ord(aString[x]) ^ ord(key[kIdx]))
        kIdx = (kIdx + 1) % len(key)
    return cryptStr

def getConfig():
    if os.path.exists(SETTINGS_FILE):
        raw = open(SETTINGS_FILE, "rb").read()
        return StringIO(mycrypt(raw, CKEY))
    else:
        return StringIO()

def saveSettings(rawConfig):
    debug("Сохраняем конфиг")
    sf = open(SETTINGS_FILE, "wb")
    sf.write(mycrypt(rawConfig, CKEY))
    sf.close()
