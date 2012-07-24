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

import platform
if platform.machine() == "i686":
    import pjsua.i686.pjsua as pj
elif platform.machine() == "x86_64":
    import pjsua.x86_64.pjsua as pj
import os
from forms.core import Core

class acc_cb(pj.AccountCallback):

    def __init__(self, account=None):
        pj.AccountCallback.__init__(self, account)
        self.core = Core()
 
    def on_reg_state(self):
        acc_info = self.account.info()   
        self.core.cb.regstate(str(acc_info.uri), str(acc_info.reg_status), str(acc_info.reg_reason))

    def on_incoming_call(self, call):
        if self.core.calls.current:
            call.answer(486, "Busy")
            return
        else:
            dev_error = False
            try:
                pass
                #self.core.dev.set_stored_dev()
                #sound_files = ["/usr/share/yass/sounds/ring.wav",
                #                os.path.join(os.path.join(os.environ['HOME'], '.yass'), "ring.wav"),
                #                os.path.join(os.path.dirname(__file__), "../../sounds/ring.wav")]

                #for sf in sound_files:
                #    if os.path.isfile(sf):
                #        self.core.cfg.player = self.core.lib.create_player(sf, True)
                #        self.core.lib.conf_connect(self.core.lib.player_get_slot(self.core.cfg.player), 0)
                #        break

            except YassException:
                dev_error = True
                self.core.dev.set_null_dev()
            finally:
                self.core.calls.current = call
                from call_cb import call_cb
                self.core.calls.current.set_callback(call_cb())        
                self.core.calls.current.answer(180)
                
                info = call.info()
                self.core.cb.incoming_call(info, dev_error)

    def on_pager(self, from_uri, contact, mime_type, body):
        #msg = yass_message(from_uri, contact, mime_type, body)
        self.core.cb.incoming_message(from_uri, contact, mime_type, body)

if __name__ == "__main__":
    pass

