# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui

class Call(QtGui.QWidget):

  def __init__(self,call, parent = None):
     QtGui.QWidget.__init__(self, parent)
     date,phone,duration,direction = call
     
     self.phone = QtGui.QLabel(phone)

     self.date = QtGui.QLabel(date)
     self.date.setStyleSheet("font-size: 10px")

     self.duration = QtGui.QLabel(str(duration))
     self.duration.setStyleSheet("font-size: 10px")

     self.direction = QtGui.QLabel(str(direction))
     self.direction.setStyleSheet("font-size: 10px")

     self.hLayout = QtGui.QHBoxLayout(self)
     self.hLayout.setSpacing(0)
     self.vLayout = QtGui.QVBoxLayout()
     self.vLayout.setSpacing(0)
     self.vLayout2 = QtGui.QVBoxLayout()
     self.vLayout2.setAlignment(QtCore.Qt.AlignRight)
     self.vLayout2.setSpacing(0)

     self.vLayout.addWidget(self.phone)
     self.vLayout.addWidget(self.date)
     self.vLayout2.addWidget(self.duration)
     self.vLayout2.addWidget(self.direction)

     self.hLayout.addLayout(self.vLayout)
     self.hLayout.addLayout(self.vLayout2)
