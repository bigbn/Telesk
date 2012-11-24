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
from forms.customWidgets import ClearLineEdit
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
from contactsitem import Contact
from database.history import HistoryAdapter
from database.contacts import ContactsAdapter
import threading
import platform
import webbrowser
#import py_pjsua

if platform.machine() == "i686":
    import pjsua.i686.pjsua as pj
elif platform.machine() == "x86_64":
    import pjsua.x86_64.pjsua as pj
elif platform.machine() == "x86":
    import pjsua.x86_win.pjsua as pj
elif platform.machine() == "darwin":
    import pjsua.i386_osx.pjsua as pj

class Dialer(formClass, BaseClass):
    def __init__(self,  parent=None):
        self.uri = ""
        self.url = "https://phonty.com/#register"
        self.callswidgets = []
        self.contactswidgets = []
        self.config = ConfigParser.RawConfigParser()
        self.config.readfp(getConfig())
        super(Dialer, self).__init__(parent)
        self.errortimer = QtCore.QTimer()
        self.errortimer.setInterval(1000)

        self.setupUi(self)
        """QPushButton,QToolButton {background-color: rgb(100,255,100); height: 20px; color: rgb(255,255,255); 
             border-style: outset; border-width: 1px; border-color: rgb(200,200,200);}"""
        self.setStyleSheet("""
                              QDialog {background: white url(:/phonty.png) no-repeat top left; color: rgb(0,0,0); border-style: outset; border-width: 1px;
                                         border-color: rgb(200,200,200);
}
                              QMessageBox {background: white }
                              QLabel {color: rgb(0,0,0);}
                              QLineEdit {color: rgb(30,30,30); background-color: rgb(255,255,255); border-style: inset; border-width: 1px;
                                         border-color: rgb(180,180,180); }""")

        self.numberEdit.button.setStyleSheet("background: transparent; border: none; margin-right: 5px")
        self.notify = NotifyManager()
        self.inactiveIcon = QtGui.QIcon(":/inactive.png")
        self.connectedIcon = QtGui.QIcon(":/connected.png")
        self.errorIcon = QtGui.QIcon(":/error.png")

        self.dialIcon = QtGui.QIcon(":/call.png")
        self.hangupIcon = QtGui.QIcon(":/stop.png")
        self.settings = SettingsForm()
 
        self.createTrayIcon()
        self.connectSignals()

        self.server = None
        self.login = None
        self.password = None
 
        try:
            self.server = self.config.get("sip", "server")
            self.login = self.config.get("sip", "login")
            self.login_edit.setText(self.login)
            self.password = self.config.get("sip", "password")
            debug(self.config.get("sip", "store"))
            if  self.config.get("sip", "store") == "True":
                self.password_edit.setText(self.password)
                self.remember_password_check.setCheckState(QtCore.Qt.Checked)
        except:
            debug("Cant get account info")
            
        self.hide_all()

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

        self.aboutAction = QtGui.QAction(QtGui.QIcon(":/about.png"), _("About"), self)
        self.menu.addAction(self.aboutAction)

        self.updateAction = QtGui.QAction(QtGui.QIcon(":/update.png"), _("Check for updates"), self)
        self.menu.addAction(self.updateAction)

        self.menu.addSeparator()
        self.quitAction = QtGui.QAction(QtGui.QIcon(":/hangup.png"), _("Quit"), self)
        self.menu.addAction(self.quitAction)
        self.tray.setContextMenu(self.menu)
        self.tray.show()

    def check_for_updates(self):
        ver_file = open(os.path.dirname(os.path.abspath(sys.argv[0]))+'/version', 'r')
        self.version = ver_file.readline()
        ver_file.close()
        version = self.phonty.version() 
        if version != self.version:
            QtGui.QMessageBox.about(self,
                                    _("New version available"),
                                    '<span>%s %s</span> <br/> <a href="%s">%s</a>' 
                                    % (_("Available version"),version,_("https://phonty.com/apps/"),_("Click here to download")))
        else:
            QtGui.QMessageBox.about(self, _("No updates available"),_("You have the latest version"))
    
    def connectSignals(self):
        sc = QtGui.QAction("Show contacts",self)
        sc.setShortcut(QtGui.QKeySequence("Alt+Up"))
        self.addAction(sc)

        hc = QtGui.QAction("Hide contacts",self)
        hc.setShortcut(QtGui.QKeySequence("Alt+Down"))
        self.addAction(hc)
 
        self.connect(self.tray, QtCore.SIGNAL("activated(QSystemTrayIcon::ActivationReason)"), self.onTrayClick)
        self.connect(self.quitAction, QtCore.SIGNAL("triggered()"), self.onQuit)
        self.connect(self, QtCore.SIGNAL('rejected()'), self.onQuit)
        
        self.connect(self.showAction, QtCore.SIGNAL("triggered()"), self.showHide)
        self.connect(self.updateAction, QtCore.SIGNAL("triggered()"), self.check_for_updates)

        self.connect(self.aboutAction, QtCore.SIGNAL("triggered()"), self.showAbout)
        self.connect(self.dialButton, QtCore.SIGNAL("clicked()"), self.makeCall)
        self.connect(self.numberEdit, QtCore.SIGNAL("returnPressed()"), self.makeCall)
        self.connect(self.login_edit, QtCore.SIGNAL("returnPressed()"), self.start_autorization)
        self.connect(self.password_edit, QtCore.SIGNAL("returnPressed()"), self.start_autorization)

        self.connect(self.hangupButton, QtCore.SIGNAL("clicked()"), self.hangup)
        self.connect(self.answerButton, QtCore.SIGNAL("clicked()"), self.answer)
        self.connect(self.rejectButton, QtCore.SIGNAL("clicked()"), self.reject_call)
        #login
        self.connect(self.login_button, QtCore.SIGNAL("clicked()"), self.start_autorization)
        
        self.connect(self.register_button, QtCore.SIGNAL("clicked()"), self.open_url)

        self.connect(self, QtCore.SIGNAL("auth_ok()"), self.finish_autoristion)
        self.connect( self, QtCore.SIGNAL("auth_wrong(QString)"), self.login_again)
        self.connect( self, QtCore.SIGNAL("autorized()"), self.load_controller_async)
        self.connect( self, QtCore.SIGNAL("controller_loaded()"), self.controller_loaded_success)

    def open_url(self):
        webbrowser.open(self.url)
        
    def login_again(self):
        self.loader.setVisible(False)
        self.result_label.setVisible(True)

    def start_autorization(self):
        self.loader.setVisible(True)
        self.result_label.setVisible(False)
        number = unicode(self.login_edit.text())
        password = unicode(self.password_edit.text())
        thread = threading.Thread(target=self.process_autorization,
                                  args=(number, password))
        thread.start()

    def process_autorization(self, number, password):
        if self.phonty.login(number, password):
            if not self.config.has_section("sip"):
                self.config.add_section("sip")
            if not self.config.has_section("main"):
                self.config.add_section("main")
            if not self.config.has_section("media"):
                self.config.add_section("media")
            self.config.set('sip', 'server',  "sip.phonty.com")
            self.config.set('sip', 'port', "6600")
            self.config.set('sip', 'login', number)
            self.config.set('sip', 'password', password)
            if self.remember_password_check.checkState():
                self.config.set('sip', 'store', True)
            else:
                self.config.set('sip', 'store', False)
            debug("Сохраняем конфигурационный файл")
            f = StringIO()
            self.config.write(f)
            saveSettings(f.getvalue())
            f.close()
            
            thread = threading.Thread(target = self.get_balance )
            thread.start()
            self.emit( QtCore.SIGNAL('auth_ok()'))
        else:
            self.emit( QtCore.SIGNAL('auth_wrong(QString)'), "auth wrong" )

    def finish_autoristion(self):
        print "i'm stat"
        self.loader.hide()
        self.login_label.setAlignment(QtCore.Qt.AlignCenter)
        self.login_label.setText("Starting. Please wait few seconds")
        self.login_edit.hide()
        self.password_label.hide()
        self.password_edit.hide()
        self.remember_password_check.hide()
        self.register_button.hide()
        self.login_button.hide()
        QtGui.qApp.processEvents()
        self.emit( QtCore.SIGNAL('autorized()'))

    #def load_controller_async(self):
    #    thread = threading.Thread(target = self.load_controller)
    #    thread.start()

    def load_controller_async(self):
        self.controller = Controller(self)
        self.emit( QtCore.SIGNAL('controller_loaded()'))
        
    def controller_loaded_success(self):
        self.login_label.hide()
        self.resize(350, 70)
        self.top_spacer.changeSize(40,50)
        self.loader_spacer.changeSize(0,0)

    def showContacts(self):
        self.fillHistoryList()
        self.fillContactsList()

    def clearHistoryList(self):
        print len(self.callswidgets)
        for widget in self.callswidgets:
            self.contactsForm.vcallsLayout.removeWidget(widget)
            widget.deleteLater()
        self.callswidgets = []

    def historycall(self,phone):
        self.numberEdit.setText(phone)

    def fillHistoryList(self):
        self.clearHistoryList()
        calls = self.calls.list()
        for call in calls:
            widget = Call(call)
            self.callswidgets.append(widget)
            self.contactsForm.vcallsLayout.addWidget(widget)
            widget.clicked.connect(self.historycall)

    def fillContactsList(self):
        #self.clearContactsList()
        contacts = self.contacts.list()

        print  "Contacs: %s" % contacts
        for contact in contacts:
            widget = Contact(contact)
            self.contactswidgets.append(widget)
            self.contactsForm.vcontactsLayout.addWidget(widget)
            widget.clicked.connect(self.historycall)

    def hideContacts(self):
        self.contactsForm.hide()
        self.contactsForm.is_hidden = True

    def showAbout(self):
        f = open(os.path.dirname(os.path.abspath(sys.argv[0]))+'/version', 'r')
        try:
            version = f.readline()
            f.close()
        except:
            version = _("Unknown version")
        about = ( version,
                 _("Phonty client based on Telesk softphone"),
                 "<a href=\"http://telesk.scat.su/\">http://telesk.scat.su</a>",
                 "Copyright (C) 2010-2012 SKAT Ltd. (<a href=\"http://www.scat.su\">http://www.scat.su</a>)",
                 "Copyright (C) 2012 Phontycom Ltd. (<a href=\"http://phonty.com\">http://phonty.com</a>)",
                 _("Translations"),
                 "Ukrainian - Maxim Nosovets (nosovetz@yandex.ua), 2012.",
                 _("""This program is free software; you can redistribute it and/or modify
                  it under the terms of the <a href="http://www.gnu.org/licenses/old-licenses/gpl-2.0.html">
                  GNU General Public License</a> as published by the Free Software Foundation;
                  either version 2 of the License, or (at your option) any later version."""))

        QtGui.QMessageBox.about(self,_("About"),"""<h1>Phonty %s</h1>
                                                    <p>%s</p>
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
        state = not self.isVisible()
        self.setVisible(state)

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
            #self.calls.outgoing(self.uri)
            #self.fillHistoryList()

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
            thread = threading.Thread(target = self.get_balance )
            thread.start()

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

    def reject_call(self):
        try:
            self.controller.reject_call()
            self.show_dialer()
        except:
            debug("Reject error")

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
        self.direction_cost_label.show()
        self.balance_label.show()
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

    def hide_all(self):
        self.direction_cost_label.hide()
        self.balance_label.hide()
        self.numberEdit.hide()
        self.dialButton.hide()
        self.callerIDLabel.hide()
        self.timerLabel.hide()
        self.hangupButton.hide()
        self.answerButton.hide()
        self.rejectButton.hide()
