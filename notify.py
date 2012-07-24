# -*- coding: utf-8 -*-
#from utils.debug import debug

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

#import ConfigParser
import sys, subprocess
#from utils.settings_file import getConfig

class NotifyManager(object):
    def __init__(self):
        self.files = {
                      "ring": [True, "sounds/ring.wav"],
                      "msg": [True, "sounds/sms.wav"],
                      "alert": [True, "sounds/alert.wav"],
                      "extorder": [True, "sounds/extorder.wav"],
        }
        self.sndcmd = "play -q %s"
#        self.loadSettings()
    
        """    def loadSettings(self):
        config = ConfigParser.RawConfigParser()
        config.readfp(getConfig())
        if config.has_section("sounds"):
            if config.has_option("sounds", "ring"):
                self.files['ring'][1] = unicode(config.get('sounds', 'ring'))
            if config.has_option("sounds", "msg"):
                self.files['msg'][1] = unicode(config.get('sounds', 'msg'))
            if config.has_option("sounds", "alert"):
                self.files['alert'][1] = unicode(config.get('sounds', 'alert'))
            if config.has_option("sounds", "extorder"):
                self.files['extorder'][1] = unicode(config.get('sounds', 'extorder'))
                
            if config.has_option("sounds", "ringenable"):
                self.files['ring'][0] = config.getboolean('sounds', 'ringenable')
            if config.has_option("sounds", "msgenable"):
                self.files['msg'][0] = config.getboolean('sounds', 'msgenable')
            if config.has_option("sounds", "alertenable"):
                self.files['alert'][0] = config.getboolean('sounds', 'alertenable')
            if config.has_option("sounds", "extorderenable"):
                self.files['extorder'][0] = config.getboolean('sounds', 'extorderenable')
            
            if config.has_option("sounds", "sndcmd"):
                self.sndcmd= unicode(config.get('sounds', 'sndcmd'))
        
        try:
            self.showTrayMsg = config.getboolean('interface', 'traynotify')
        except:
            debug("Настройку по сообщения в трее загрузить не удалось")"""
            
    def playSound(self, f):
        if sys.platform.startswith("win"):
            import winsound
            winsound.PlaySound(f, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            subprocess.Popen(self.sndcmd % (f), shell=True)
    
    def sound(self, eid):
        if eid not in self.files:
            debug(u"События %s не определено" % eid)
            return
        if self.files[eid][0]: self.playSound(self.files[eid][1])
    
    """    def tray(self, title, message, duration=5000):
        if self.showTrayMsg:
            self.form.tray.showMessage(title, message, QtGui.QSystemTrayIcon.Information, duration)"""
