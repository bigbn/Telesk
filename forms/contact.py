# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class ContactEditor(QtGui.QDialog):
    def __init__(self, phonty=None, id = None , name = '', phone = ''):

        self.id = id
        self.phonty = phonty
        self.name = name
        self.phone = phone

        QtGui.QDialog.__init__(self)

        self.resize(350, 200)

        self.nameLabel = QtGui.QLabel(self)
        self.nameLabel.setText(_("Contact name"))
        self.textName = QtGui.QLineEdit(self)
        self.phoneLabel = QtGui.QLabel(self)
        self.phoneLabel.setText(_("Phone number"))
        self.textPhone = QtGui.QLineEdit(self)

        self.buttonsLayout = QtGui.QHBoxLayout()
        self.buttonCancel = QtGui.QPushButton(_('Cancel'), self)
        self.buttonCancel.clicked.connect(self.reject)

        self.buttonSave = QtGui.QPushButton(_('Save'), self)
        self.buttonSave.clicked.connect(self.handleForm)

        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.nameLabel)
        layout.addWidget(self.textName)
        layout.addWidget(self.phoneLabel)
        layout.addWidget(self.textPhone)

        layout.addLayout(self.buttonsLayout)
        self.buttonsLayout.addWidget(self.buttonCancel)
        self.buttonsLayout.addWidget(self.buttonSave)

        if self.id:
            self.textName.setText(self.name)
            self.textPhone.setText(self.phone)

    def getValues(self):
        return (self.id, self.name, self.phone)

    def handleForm(self):
        if self.id:
            if self.phonty.contact_edit(self.id, self.textName.text(), self.textPhone.text()):
                self.name = self.textName.text()
                self.phone = self.textPhone.text()
                self.accept()
            else:
                QtGui.QMessageBox.warning(self, _('Error'), _('Something wrong'))
        else:
            if self.phonty.contact_add(self.textName.text(), self.textPhone.text()):
                self.id = self.phonty.result
                self.accept()
            else:
                QtGui.QMessageBox.warning(self, _('Error'), _('Something wrong'))