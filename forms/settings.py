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

from PyQt4 import QtCore, QtGui
BaseClass = QtGui.QDialog
from ui_settings import Ui_SettingsDialog as formClass
import sys
from debug import debug
import os
from StringIO import StringIO

from settings_file import getConfig, saveSettings
import ConfigParser
config = ConfigParser.RawConfigParser()
config.readfp(getConfig())
import traceback

def reset_config():
    config.readfp(getConfig())

class SettingsForm(formClass, BaseClass):
    def __init__(self,  parent=None):
        super(SettingsForm, self).__init__(parent)
        self.setupUi(self)

    def load(self, checkpass = True):
        reset_config()
        try:
            self.serverEdit.setText(unicode(config.get("sip", "server")))
            self.portEdit.setText(unicode(config.get("sip", "port")))
            self.loginEdit.setText(unicode(config.get("sip", "login")))
            self.passwordEdit.setText(unicode(config.get("sip", "password")))

            self.aaCheckBox.setChecked(config.getboolean("main", "aa"))
            self.aotCheckBox.setChecked(config.getboolean("main", "aot"))
            self.ustcheckBox.setChecked(config.getboolean("main", "ust"))

            self.inputComboBox.setCurrentIndex(config.getint("media", "input"))
            self.outputComboBox.setCurrentIndex(config.getint("media", "output"))
        except:
            self.inputComboBox.setCurrentIndex(self.inputComboBox.findText("default"))
            self.outputComboBox.setCurrentIndex(self.outputComboBox.findText("default"))
            #debug(traceback.format_exc())
            self.show()
            return False
        return True

    def save(self):
        if not config.has_section("sip"):
            config.add_section("sip")
        if not config.has_section("main"):
            config.add_section("main")
        if not config.has_section("media"):
            config.add_section("media")
        config.set('sip', 'server',  unicode(self.serverEdit.text()))
        config.set('sip', 'port',  unicode(self.portEdit.text()))
        config.set('sip', 'login',  unicode(self.loginEdit.text()))
        config.set('sip', 'password',  unicode(self.passwordEdit.text()))

        config.set("main", "aa", self.aaCheckBox.isChecked())
        config.set("main", "aot", self.aotCheckBox.isChecked())
        config.set("main", "ust", self.ustcheckBox.isChecked())
        config.set("media", "input", self.inputComboBox.currentIndex())
        config.set("media", "output", self.outputComboBox.currentIndex())

        debug("Сохраняем конфигурационный файл")
        f = StringIO()
        config.write(f)
        saveSettings(f.getvalue())
        f.close()
