#!/usr/bin/python
# -*- coding: utf-8 -*-

method = "cxfreeze" # "py2exe"

if method == "py2exe":
    print "py2exe"
    from distutils.core import setup
    import py2exe 
    setup(
          windows=[{"script" : "main.py", "icon_resources": [(0, "ico.ico")]}],
          options={
                   "py2exe" : {
                               "compressed": 2,
                               "optimize": 2,
                               "dll_excludes": ['tcl85.dll', 'tk85.dll'],
                               "includes" : ["sip", "xml.etree.cElementTree", "resource_rc"],
                               "excludes" : ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs',"Tkconstants","Tkinter","tcl"],
                               }
                   },
    )

elif method == "cxfreeze":
    print "cxfreeze"
    from cx_Freeze import setup, Executable, Freezer
    exe = Executable(
        script="main.py",
        targetName="telesk.exe"
    )
    freezer = Freezer([exe],
        base = "Win32GUI",
        icon = "images\\telesk_default.ico",
        #compress = True,
        path = None,
        createLibraryZip = False,
        #copyDependentFiles =True,
        appendScriptToExe = True,
        #appendScriptToLibrary = True,
        targetDir = 'dist',
        #includes = ["sqlalchemy.dialects.mysql", "PyQt4.QtNetwork"],
        excludes = ['_gtkagg', '_tkagg', 'bsddb', 'curses', 'email', 'pywin.debugger', 'pywin.debugger.dbgcon', 'pywin.dialogs',"Tkconstants","Tkinter","tcl"]
    )
    freezer.Freeze()
    """setup(
        name = "Telesk",
        version = "0.2",
        description = "Telesk Softphone by SKAT LTD",
        executables = [exe]
    )"""