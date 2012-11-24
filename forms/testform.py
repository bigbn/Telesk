# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from login import LoginForm


def main():
    app = QtGui.QApplication(sys.argv)
    w = LoginForm()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
