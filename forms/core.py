# -*- coding: utf-8 -*-

# Copyright 2008, 2009 Saúl Ibarra <saghul@gmail.com>
# Copyright (C) 2010-2012 SKAT Ltd. (http://www.scat.su)

# This file is part of YASS.
#
# YASS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# YASS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with YASS.  If not, see <http://www.gnu.org/licenses/>.



import platform
if platform.machine() == "i686":
    import pjsua.i686.pjsua as pj
elif platform.machine() == "x86_64":
    import pjsua.x86_64.pjsua as pj
elif platform.machine() == "x86":
    import pjsua.x86_win.pjsua as pj	
	
import sys
import threading
from debug import debug
from call import Call
from core_callbacks import core_cb
from settings_file import getConfig, saveSettings
import ConfigParser
import socket


class Core(object):

    ## Class for holding the *real* core implementation.
    class __impl(object):

        ## Getters/setters
        def _get_lib(self):
            return self._lib

        def _set_lib(self, lib):
            self._lib = lib

        lib = property(_get_lib, _set_lib)

        def _get_transport(self):
            return self._transport

        def _set_transport(self, transport):
            self._transport = transport

        transport = property(_get_transport, _set_transport)

        def _get_acc(self):
            return self._acc

        def _set_acc(self, acc):
            self._acc = acc

        acc = property(_get_acc, _set_acc)

        def _get_cb(self):
            return self._cb

        def _set_cb(self, cb):
            self._cb = cb

        cb = property(_get_cb, _set_cb)

        def _get_dev(self):
            return self._dev

        def _set_dev(self, dev):
            self._dev = dev

        dev = property(_get_dev, _set_dev)


        ## Start/stop/reload the core.
        def start(self):

            self.config = ConfigParser.RawConfigParser()
            self.config.readfp(getConfig())
            self._start_lib()
            self._start_acc()
            #except pj.Error:
            #    debug("Error starting the core.")

        def stop(self):
            try:
                self.lib.hangup_all()
                self._stop_acc()
                self.transport = None
                self._stop_lib()
            except pj.Error:
                debug("Error stoping the core.")

        def restart_core(self):
            try:
                self.stop()
                self.lib = pj.Lib()
                self.start()
            except pj.Error:
                debug("Error restarting the core.")

        def _bind(self):
            try:
                self.transport = self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig(5060)) #int(self.config.get("sip", "port"))))
            except pj.Error:
                debug(pj.Error)

        def _start_lib(self):
            self.lib.init()
            self._bind()
            self.lib.start()
            #self.dev = yass_devices(self.lib)
            #codecs.load_codecs()

        def _stop_lib(self):
            if self.lib:
                self.lib.destroy()
                self.lib = None
            self.dev = None

        def _start_acc(self):
            from callback.acc_cb import acc_cb
            try:
                print unicode(self.config.get("sip", "server"))
                print self.config.get("sip", "login")
                print self.config.get("sip", "password")
                self.proxy = socket.gethostbyname(unicode(self.config.get("sip", "server")))
                self.acc = self.lib.create_account(acc_config=pj.AccountConfig(self.proxy, self.config.get("sip", "login"),self.config.get("sip", "password")), cb=acc_cb())
            except pj.Error:
                debug("Error creating account.")

        def _stop_acc(self):
            if self.acc is not None:
                self.acc.delete()

        def restart_acc(self):
            self._stop_acc()
            self.cfg.reload_acc()
            self._start_acc()


        ## Telephony related functions.
        def make_call(self, num):
            if self.calls.current:
                pass
            else:
                try:
                    #self.dev.set_stored_dev()

                    from callback.call_cb import call_cb
                    call = self.acc.make_call("sip:%s@%s" % (num.encode("utf-8"),self.proxy),cb=call_cb())
                    self.calls.current = call
                except pj.Error:
                    debug("Couldn't make the call.")

        def answer_call(self, call):
            if call:
                call.answer()
            else:
                debug("Not an active call.")

        def hangup_call(self, call):
            if call:
                call.hangup()
            else:
                debug("Not an active call.")

        def reject_call(self, call):
            if call:
                call.answer(486, "Busy")
            else:
                debug("Not an active call.")

        def hold_call(self, call):
            if call:
                call.hold()
            else:
                debug("Not an active call.")

        def unhold_call(self, call):
            if call:
                call.unhold()
            else:
                debug("Not an active call.")

        def send_dtmf(self, call, digit):
            if call:
                try:
                    call.dial_dtmf(digit)
                except pj.Error:
                    pass
            else:
                debug("Not an active call.")

        def blind_xfer(self, call, dst):
            try:
                dsturi = sip_utils.make_uri(dst, self.cfg.acc.acc.acc_domain)
                call.transfer(str(dsturi))
                call.hangup()
            except pj.Error:
                debug("Error during call transfer.")


        def __init__(self):
            try:
                self.lib = pj.Lib()
            except pj.Error:
                debug("Error initialising library.")

            self.calls = Call()
            self.cb = core_cb()
            self.transport = None
            self.acc = None
            self.dev = None


    ## Private attributes for holding the instance and the lock.
    __instance = None
    __lock = threading.Lock()


    ## Initialize the ONLY core instance (if needed).
    def __init__(self):
        Core.__lock.acquire(True)
        try:
            if Core.__instance is None:
                Core.__instance = Core.__impl()
        finally:
            Core.__lock.release()


    ## Delegate access to implementation.
    def __getattr__(self, attr):
        return getattr(self.__instance, attr)

    ## Delegate access to implementation.
    def __delattr__(self, attr):
        return delattr(self.__instance, attr)

    ## Delegate access to implementation.
    def __setattr__(self, attr, value):
        return setattr(self.__instance, attr, value)


if __name__ == "__main__":
    pass

