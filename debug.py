# -*- coding: utf-8 -*-

# Copyright (C) 2010-2012 SKAT Ltd. (http://www.scat.su)
# Copyright (C) 2011-2013 PHONTYCOM Ltd. (http://www.phonty.com)

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

import sys
import logging
from datetime import datetime

if "-d" in sys.argv:
    DEBUG = True
else:
    DEBUG = False


def debug(message):
    try:
        if DEBUG: 
            if type(message) == unicode:
                message = message.encode("utf-8")
            write(message)

    except:
        print "Error whyle debugging"


def write(message):
    logging.debug("%s %s" % (datetime.now().strftime("%d.%m %H:%M:%S"), message))

