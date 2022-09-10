#
# Created on Thu Aug 11 2022 10:35:41 PM
#
# The MIT License (MIT)
# Copyright (c) 2022 Aananth C N
#
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software
# and associated documentation files (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
# TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
#
import os
import sys

from gui.lib.main_view import FreeAutosarConfTool


def main(fpath, ftype):
    # Create the main window
    Gui = FreeAutosarConfTool()

    # setup initial view (AUTOSAR view is the default, now)
    Gui.init_view_setup(fpath, ftype)

    # Run forever!
    Gui.main_view.tk.mainloop()


#
# Arguments to osek-builder-gui.py if invoked from command-line
#
# -f: "file name with path to open"
# -t: filetype ["oil", "arxml"]
#
if __name__ == '__main__':
    filepath = None
    filetype = None

    # collect the arguments if it is passed as arguments
    if "-f" in sys.argv:
        filepath = sys.argv[sys.argv.index("-f") + 1]
        filepath = os.path.abspath(filepath)
        filepath = filepath.replace(os.sep, '/')
        # set source code generation path
        srcpath = filepath.split("NammaAUTOSAR")[0]+"NammaAUTOSAR/tools/src"
        sg.set_source_file_path(srcpath)
    if "-t" in sys.argv:
        filetype = sys.argv[sys.argv.index("-t") + 1]
    
    # let us start the GUI
    main(fpath=filepath, ftype=filetype)