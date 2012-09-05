# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Contact(QtGui.QWidget):
  clicked = QtCore.pyqtSignal(['QString'])

  def __init__(self,contact, parent = None):
     QtGui.QWidget.__init__(self, parent)
     _id,id,name,phone = contact

     self.name = name
     self.name = QtGui.QLabel(name)
     self.name.setStyleSheet("font-size: 15px")

     self.phone = QtGui.QLabel(phone)
     self.phone.setStyleSheet("font-size: 10px")

     self.hLayout = QtGui.QHBoxLayout(self)
     self.hLayout.setSpacing(0)
     self.vLayout = QtGui.QVBoxLayout()
     self.vLayout.setSpacing(0)
     self.vLayout2 = QtGui.QVBoxLayout()
     self.vLayout2.setAlignment(QtCore.Qt.AlignRight)
     self.vLayout2.setSpacing(0)

     self.vLayout.addWidget(self.name)
     self.vLayout.addWidget(self.phone)

     self.hLayout.addLayout(self.vLayout)
     self.hLayout.addLayout(self.vLayout2)
     
  def mousePressEvent(self, event):
     self.phonenum = self.phone.text()
     self.setFocus(QtCore.Qt.OtherFocusReason)
     event.accept()
    
  def mouseReleaseEvent(self, event):
     if event.button() == QtCore.Qt.LeftButton:
       self.update()
       phone = str(self.phone.text())
       number = phone[phone.index(":")+1:phone.index("@")]
       self.clicked.emit(number)
       event.accept()
