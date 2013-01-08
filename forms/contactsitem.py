# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s
from contact import ContactEditor

class Contact(QtGui.QWidget):
  clicked = QtCore.pyqtSignal(['QString'])
  makeCall = QtCore.pyqtSignal(['QString'])

  def __init__(self, contact, phonty, parent = None):
     QtGui.QWidget.__init__(self, parent)
     self.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
     self.phonty = phonty
     self.id = contact["id"]
     self.name = contact["name"]
     self.nameLabel = QtGui.QLabel(self.name)
     self.nameLabel.setStyleSheet("font-size: 15px")

     self.phone = contact["phone"]
     self.phoneLabel = QtGui.QLabel(self.phone)
     self.phoneLabel.setStyleSheet("font-size: 10px")

     self.callButton = QtGui.QToolButton(self)
     self.callButton.setCursor(QtCore.Qt.ArrowCursor)
     self.callButton.setFocusPolicy(QtCore.Qt.NoFocus)

     call_icon = QtGui.QIcon()
     call_icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/call_mini.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)

     self.callButton.setIcon(call_icon)
     self.callButton.setStyleSheet("border: none;")
     self.callButton.clicked.connect(self.make_call)

     self.hLayout = QtGui.QHBoxLayout(self)
     self.hLayout.setSpacing(0)
     self.vLayout = QtGui.QVBoxLayout()
     self.vLayout.setSpacing(0)
     self.vLayout2 = QtGui.QVBoxLayout()
     self.vLayout2.setAlignment(QtCore.Qt.AlignRight)
     self.vLayout2.setSpacing(0)

     self.vLayout.addWidget(self.nameLabel)
     self.vLayout.addWidget(self.phoneLabel)

     self.hLayout.addWidget(self.callButton)

     self.hLayout.addLayout(self.vLayout)
     self.hLayout.addLayout(self.vLayout2)

  def mousePressEvent(self, event):
     self.phonenum = self.phone
     self.setFocus(QtCore.Qt.OtherFocusReason)
     event.accept()

  def make_call(self):
      self.makeCall.emit(self.phone)

  def contextMenuEvent(self, event):
     """
     Context menu handling
     """
     menu = QtGui.QMenu(self)
     callAction = menu.addAction(u"Вызов")
     #smsAction = menu.addAction(u"Отправить СМС")
     editAction = menu.addAction(u"Редактировать")
     deleteAction = menu.addAction(u"Удалить")
     menu.addSeparator()
     addAction = menu.addAction(u"Добавить контакт")

     action = menu.exec_(self.mapToGlobal(event.pos()))

     if action == deleteAction:
        if self.phonty.contact_delete(self.id):
            self.deleteLater()
            self = None

     elif action == callAction:
         self.make_call()

     elif action == addAction:
         editor = ContactEditor(phonty = self.phonty)
         if editor.exec_() == QtGui.QDialog.Accepted:
             self.addItem(editor.getValues())

     elif action == editAction:
         editor = ContactEditor(phonty = self.phonty, id = self.id, name= self.name, phone = self.phone)
         if editor.exec_() == QtGui.QDialog.Accepted:
             self.updateItem(editor.getValues())

  def updateItem(self,values):
      self.id,self.name,self.phone = values
      self.nameLabel.setText(self.name)
      self.phoneLabel.setText(self.phone)

  def addItem(self,values):
      self.id,self.name,self.phone = values
      #TODO: Вызвать метод родителя

  def mouseReleaseEvent(self, event):
     """
     Mouse release event
     """
     if event.button() == QtCore.Qt.LeftButton:
       self.update()
       self.clicked.emit(self.phone)
       event.accept()