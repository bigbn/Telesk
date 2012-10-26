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

class core_cb(object):
    """ Container for callbacks to be called by the core:
            * regstate: It's called when the registry state changes.
            * incoming_call: It's called when an incoming call is received.
            * incoming_message: It's called when an incoming MESSAGE request is received.
            * callstate: It's called when a call's state is changed.
            * medistate: It's called when the media state is changed.
            * buddystate: It's called when a buddy's state is changed.
            * hangup: It's called when a call is hung up.
    """

    def set_cb_regstate(self, func):
        self._regstate = func

    def regstate(self, *args, **kwargs):
        if hasattr(self, "_regstate") and callable(self._regstate):
            self._regstate(*args, **kwargs)

    def set_cb_incoming_call(self, func):
       self._incoming_call = func

    def incoming_call(self, *args, **kwargs):
        if hasattr(self, "_incoming_call") and callable(self._incoming_call):
            self._incoming_call(*args, **kwargs)

    def set_cb_incoming_message(self, func):
       self._incoming_message = func

    def incoming_message(self, *args, **kwargs):
        if hasattr(self, "_incoming_message") and callable(self._incoming_message):
            self._incoming_message(*args, **kwargs)

    def set_cb_callstate(self, func):
       self._callstate = func

    def callstate(self, *args, **kwargs):
        if hasattr(self, "_callstate") and callable(self._callstate):
            self._callstate(*args, **kwargs)

    def set_cb_mediastate(self, func):
       self._medistate = func

    def mediastate(self, *args, **kwargs):
        if hasattr(self, "_mediastate") and callable(self._medistate):
            self._medistate(*args, **kwargs)

    def set_cb_buddystate(self, func):
       self._buddystate = func

    def buddystate(self, *args, **kwargs):
        if hasattr(self, "_buddystate") and callable(self._buddystate):
            self._buddystate(*args, **kwargs)

    def set_cb_hangup(self, func):
        self._hangup = func

    def hangup(self, *args, **kwargs):
        if hasattr(self, "_hangup") and callable(self._hangup):
            self._hangup(*args, **kwargs)

    def __init__(self):
        pass

if __name__ == "__main__":
    pass

