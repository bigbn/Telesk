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
from ui_dialDialog import Ui_DialWindow as formClass
import sys
from debug import debug
import os
from StringIO import StringIO
from settings_file import getConfig, saveSettings
from forms.settings import SettingsForm
import ConfigParser
import resource_rc
from controller import Controller
from notify import NotifyManager
from contacts import ContactsForm
from historyitem import Call
from database.history import HistoryAdapter

class Dialer(formClass, BaseClass):
    def __init__(self,  parent=None):
        self.uri = ""
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(getConfig())
        super(Dialer, self).__init__(parent,QtCore.Qt.FramelessWindowHint)
        self.errortimer = QtCore.QTimer()
        self.errortimer.setInterval(1000)
        self.setupUi(self)
        try:
            if self.config.getboolean("main", "aot"):
                self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        except:
            pass

        try:
            if not self.config.getboolean("main", "ust"):
                a=1/0
            else:
                self.dialButton.setIcon(QtGui.QIcon.fromTheme("call-start"))
                self.hangupButton.setIcon(QtGui.QIcon.fromTheme("call-stop"))
        except:
            self.setStyleSheet("""QPushButton,QToolButton {background-color: rgb(40,40,40); height: 20px; color: rgb(255,255,255);  border-style: outset; border-width: 1px;
                              border-color: rgb(50,50,50);}
                              QDialog {background-color: rgb(10,10,10); color: rgb(255,255,255); border-style: outset; border-width: 1px;
                                         border-color: rgb(50,50,50);
}
                              QLabel {color: rgb(255,255,255);}
                              QLineEdit {color: white; background-color: rgb(30,30,30); border-style: outset; border-width: 1px;
                                         border-color: rgb(50,50,50); }""")


        self.contactsForm = ContactsForm()
        self.numberEdit.button.setStyleSheet("background: transparent; border: none; margin-right: 5px")
        self.notify = NotifyManager()
        self.inactiveIcon = QtGui.QIcon(":/inactive.png")
        self.connectedIcon = QtGui.QIcon(":/connected.png")
        self.errorIcon = QtGui.QIcon(":/error.png")
        
        self.dialIcon = QtGui.QIcon(":/call.png")
        self.hangupIcon = QtGui.QIcon(":/stop.png")
        self.settings = SettingsForm()
        self.controller = Controller(self)
        self.settings.load()
        self.createTrayIcon()
        self.connectSignals()

        self.server = None
        self.login = None
        self.password = None
        
        self.calls = HistoryAdapter()

        try:
            self.server = self.config.get("sip", "server")
            self.login = self.config.get("sip", "login")
            self.password = self.config.get("sip", "password")
        except:
            pass
        for sd in self.controller.core.lib.enum_snd_dev():
            self.settings.inputComboBox.addItem(self.trans(sd.name))
            self.settings.outputComboBox.addItem(self.trans(sd.name))
        self.settings.load()
        try:
            self.controller.core.lib.set_snd_dev(self.settings.inputComboBox.currentIndex(), self.settings.outputComboBox.currentIndex())
        except:
            debug(_("Audio-device error"))

    def trans(self,string):
        if not sys.platform.startswith("win"):
            return string
        else:
            return unicode(string.decode("CP1251"))


    def createTrayIcon(self):
        # Создаем иконку в трее
        icon = QtGui.QIcon(":/inactive.png")
        
        self.setWindowIcon(icon)
        self.tray = QtGui.QSystemTrayIcon(icon, self)

        self.menu =QtGui.QMenu(self)
        self.showAction = QtGui.QAction(_("Activate"), self)
        self.menu.addAction(self.showAction)
        self.settingsAction = QtGui.QAction(QtGui.QIcon(":/settings.png"), _("Settings"), self)
        self.menu.addAction(self.settingsAction)
        
        self.aboutAction = QtGui.QAction(QtGui.QIcon(":/about.png"), _("About"), self)
        self.menu.addAction(self.aboutAction)
        
        self.menu.addSeparator()
        self.quitAction = QtGui.QAction(QtGui.QIcon(":/shutdown.png"), _("Quit"), self)
        self.menu.addAction(self.quitAction)

        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def connectSignals(self):

        sc = QtGui.QAction("Show contacts",self)
        sc.setShortcut(QtGui.QKeySequence("Alt+Up"))
        self.addAction(sc)
        
        hc = QtGui.QAction("Hide contacts",self)
        hc.setShortcut(QtGui.QKeySequence("Alt+Down"))
        self.addAction(hc)
        
        sc.triggered.connect(self.showContacts)
        hc.triggered.connect(self.hideContacts)
        
        self.connect(self.tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.onTrayClick)
        self.connect(self.quitAction, QtCore.SIGNAL("triggered()"), self.onQuit)
        self.connect(self.showAction, QtCore.SIGNAL("triggered()"), self.showHide)
        self.connect(self.settingsAction, QtCore.SIGNAL("triggered()"), self.settings.show)
        self.connect(self.aboutAction, QtCore.SIGNAL("triggered()"), self.showAbout)
        self.connect(self.settings, QtCore.SIGNAL("accepted()"), self.settings.save)
        self.connect(self.settings, QtCore.SIGNAL("accepted()"), self.reload)
        self.connect(self.dialButton, QtCore.SIGNAL("clicked()"), self.makeCall)
        self.connect(self.numberEdit, QtCore.SIGNAL("returnPressed()"), self.makeCall)
        self.connect(self.hangupButton, QtCore.SIGNAL("clicked()"), self.hangup)
        self.connect(self.answerButton, QtCore.SIGNAL("clicked()"), self.answer)
        self.connect(self.rejectButton, QtCore.SIGNAL("clicked()"), self.reject)

    def showContacts(self):
        print "ok"
        self.contactsForm.show()
        calls = self.calls.list()
        print calls
        for call in calls:
            widget = Call(call)
            self.contactsForm.vcallsLayout.addWidget(widget)


    def hideContacts(self):
        print "ok"
        self.contactsForm.hide()

    def showAbout(self):
        try:
            f = open(os.path.dirname(os.path.abspath(sys.argv[0]))+'/version', 'r')
            version = f.readline()
            f.close()
        except:
            version = _("Unknown version")
        about = ( version,
                 _("QT and PJSIP based minimalistic SIP Client"),
                 "<a href=\"https://github.com/bigbn/Telesk\">https://github.com/bigbn/Telesk</a>",
                 "Copyright (C) 2010-2012 SKAT Ltd. (<a href=\"http://www.scat.su\">http://www.scat.su</a>)",
                 _("Translations"),
                 "Ukrainian - Maxim Nosovets (nosovetz@yandex.ua), 2012.",
                 _("""This program is free software; you can redistribute it and/or modify
                  it under the terms of the <a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">
                  GNU General Public License</a> as published by the Free Software Foundation; 
                  either version 2 of the License, or (at your option) any later version."""))

        QtGui.QMessageBox.about(self,_("About"),"""<h1>Telesk %s</h1>
                                                    <p>%s</p>
                                                    <p>%s</p>
                                                    <p>%s</p>
                                                    <p><b>%s:</b><br/>
                                                    %s</p>
                                                    <p>%s</p>                                                    
                                                    """ % about)

    def reload(self):
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(getConfig())
        self.tray.setIcon(self.inactiveIcon)
        self.controller.core.restart_core()
        if self.config.getboolean("main", "aot"):
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        else:
            self.setWindowFlags(QtCore.Qt.FramelessWindowHint)

    def showHide(self):
        if sys.platform.startswith("win"):
            right = QtGui.QDesktopWidget().availableGeometry().width()-self.frameSize().width()
            bottom = QtGui.QDesktopWidget().availableGeometry().height()-self.frameSize().height()
        else:
            right = QtGui.QDesktopWidget().availableGeometry().width()-self.frameSize().width()/2
            bottom = QtGui.QDesktopWidget().availableGeometry().height()-self.frameSize().height()/2
        self.move(right, bottom)
        self.setVisible(not self.isVisible())

    def onTrayClick(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            self.showHide()

    def onQuit(self):
        debug(_("Exiting"))
        self.tray.hide()
        sys.exit(0)

    def makeCall(self):
        number = unicode(self.numberEdit.text())
        if number.strip() != "":
            self.controller.make_call(number)


    def hangup(self):
        self.controller.hangup_call()
        self.numberEdit.show()
        self.dialButton.show()
        self.callerIDLabel.hide()
        self.timerLabel.hide()
        self.hangupButton.hide()

    @QtCore.pyqtSlot(str,str,int,str)
    def onStateChange(self, uri, state, code, reason):
        debug("Call state: %s %s %s" % (uri, state, code))
        self.uri = uri
        self.callerIDLabel.setText(self.uri)
        if state == "CALLING" or state == "CONNECTING":
            self.show_error(_("Calling..."))
            self.dialButton.hide()
            self.hangupButton.show()


        if state == "CONFIRMED":
            self.seconds = 0
            self.callerIDLabel.setText(self.uri)
            self.timerLabel.setText(u"0:00")
            self.setWindowTitle(_("Call in process"))
            self.startTimer()
            self.show_call()
            self.calls.outgoing(self.uri)
            
        if state == "DISCONNCTD":
            self.setWindowTitle(_("Telesk"))
            self.timerLabel.setText(u"0:00")
            if code == 503:
                self.show_error(_("Not available"))
            if code == 404:
                self.show_error(_("Not found"))
            if code == 486:
                self.show_error(_("Busy here"))
            if code == 603:            
                self.show_error(_("Decline"))
                
            self.errortimer.start()
            self.connect(self.errortimer, QtCore.SIGNAL("timeout()"), self.show_dialer)

    @QtCore.pyqtSlot()
    def onRegister(self):
        self.tray.setIcon(self.connectedIcon)
        self.show_dialer()
        
    @QtCore.pyqtSlot()
    def onRegisterFailed(self):
        self.tray.setIcon(self.errorIcon)
        self.show_error(_("SIP registration failed"))

    @QtCore.pyqtSlot()
    def onIncomingCall(self):
        self.setVisible(True)
        if self.config.getboolean("main", "aa"):
            self.answer()
        else:
            self.notify.sound("ring")
            self.show_incoming()

    def answer(self):
        self.controller.answer_call()
        self.show_call()

    def reject(self):
        self.controller.reject_call()
        self.show_dialer()

    def show_dialer(self):        
        self.seconds = 0
        self.timer.stop()
        self.errortimer.stop()
        self.answerButton.hide()
        self.rejectButton.hide()
        self.numberEdit.show()
        self.dialButton.show()
        self.callerIDLabel.hide()
        self.timerLabel.hide()
        self.hangupButton.hide()
        self.update()

    def show_call(self):
        self.answerButton.hide()
        self.rejectButton.hide()
        self.numberEdit.hide()
        self.dialButton.hide()
        self.callerIDLabel.show()
        self.timerLabel.show()
        self.hangupButton.show()
        self.update()

    def show_incoming(self):
        self.numberEdit.hide()
        self.dialButton.hide()
        self.callerIDLabel.show()
        self.timerLabel.hide()
        self.hangupButton.hide()
        self.answerButton.show()
        self.rejectButton.show()
        self.update()
        
    def show_error(self,error):
        self.numberEdit.hide()
        self.dialButton.show()
        self.callerIDLabel.show()
        self.timerLabel.hide()
        self.hangupButton.hide()
        self.answerButton.hide()
        self.rejectButton.hide()
        self.callerIDLabel.setText(unicode(error))
        self.update()
